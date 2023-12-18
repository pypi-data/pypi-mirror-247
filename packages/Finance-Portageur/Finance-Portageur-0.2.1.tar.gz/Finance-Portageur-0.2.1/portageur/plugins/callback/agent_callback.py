import time, json, pdb
from typing import Any, Optional
from uuid import UUID
from langchain.agents import openai_functions_agent, openai_functions_multi_agent
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult, ChatGeneration, BaseMessage
from portageur.plugins.callback.entity.agent_loop import AgentLoop
from portageur.plugins.callback.entity.message import PromptMessage

class AgentCallbackHandler(BaseCallbackHandler):
    def __init__(self, model_instance):
        """Initialize callback handler."""
        self.model_instance = model_instance
        self._agent_loops = []
        self._current_loop = None
        self._message_agent_thought = None
        self.current_chain = None
        self.completion_tokens = 0
        self.prompt_tokens = 0
    
    @property
    def agent_loops(self):
        return self._agent_loops

    def clear_agent_loops(self) -> None:
        self._agent_loops = []
        self._current_loop = None
        self._message_agent_thought = None

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True
    
    @property
    def ignore_chain(self) -> bool:
        """Whether to ignore chain callbacks."""
        return True
    

    def on_llm_start(self, serialized, prompts, **kwargs):
        if not self._current_loop:
            # Agent start with a LLM query
            self._current_loop = AgentLoop(
                position=len(self._agent_loops) + 1,
                prompt=prompts[0],
                status='llm_started',
                started_at=time.perf_counter()
            )

    def on_llm_end(self, response, **kwargs):
        if self._current_loop and self._current_loop.status == 'llm_started':
            self._current_loop.status = 'llm_end'
            if response.llm_output:
                self._current_loop.prompt_tokens = response.llm_output['token_usage']['prompt_tokens']
            else:
                self._current_loop.prompt_tokens = self.model_instance.get_num_tokens(
                    [PromptMessage(content=self._current_loop.prompt)]
                )
            completion_generation = response.generations[0][0]
            if isinstance(completion_generation, ChatGeneration):
                completion_message = completion_generation.message
                if 'function_call' in completion_message.additional_kwargs:
                    self._current_loop.completion \
                        = json.dumps({'function_call': completion_message.additional_kwargs['function_call']})
                else:
                    self._current_loop.completion = response.generations[0][0].text
            else:
                self._current_loop.completion = completion_generation.text
            
            if response.llm_output:
                self._current_loop.completion_tokens = response.llm_output['token_usage']['completion_tokens']
            else:
                self._current_loop.completion_tokens = self.model_instance.get_num_tokens(
                    [PromptMessage(content=self._current_loop.completion)]
                )
            self.prompt_tokens += self._current_loop.prompt_tokens
            self.completion_tokens += self._current_loop.completion_tokens

    def on_llm_error(self, error, **kwargs):
        self._agent_loops = []
        self._current_loop = None
        self._message_agent_thought = None

    def on_agent_action(self, action, color= None, **kwargs):
        tool = action.tool
        tool_input = json.dumps({"query": action.tool_input}
                                if isinstance(action.tool_input, str) else action.tool_input)
        completion = None
        try:
            action_name_position = action.log.index("action:") if action.log else -1
            thought = action.log[:action_name_position].strip() if action.log else ''
        except:
            thought = ''

        
        if self._current_loop and self._current_loop.status == 'llm_end':
            self._current_loop.status = 'agent_action'
            self._current_loop.thought = thought
            self._current_loop.tool_name = tool
            self._current_loop.tool_input = tool_input
            if completion is not None:
                self._current_loop.completion = completion

    def on_tool_end(self, output, color, observation_prefix, llm_prefix, **kwargs):
        if self._current_loop and self._current_loop.status == 'agent_action' and output and output != 'None':
            self._current_loop.status = 'tool_end'
            self._current_loop.tool_output = output
            self._current_loop.completed = True
            self._current_loop.completed_at = time.perf_counter()
            self._current_loop.latency = self._current_loop.completed_at - self._current_loop.started_at

            #self.conversation_message_task.on_agent_end(
            #    self._message_agent_thought, self.model_instance, self._current_loop
            #)

            self._agent_loops.append(self._current_loop)
            self._current_loop = None
            self._message_agent_thought = None

    def on_tool_error(self, error, **kwargs):
        """Do nothing."""
        self._agent_loops = []
        self._current_loop = None
        self._message_agent_thought = None

    def on_agent_finish(self, finish, **kwargs):
        if self._current_loop and (self._current_loop.status == 'llm_end' or self._current_loop.status == 'agent_action'):
            self._current_loop.status = 'agent_finish'
            self._current_loop.completed = True
            self._current_loop.completed_at = time.perf_counter()
            self._current_loop.latency = self._current_loop.completed_at - self._current_loop.started_at
            self._current_loop.thought = '[DONE]'

            self._agent_loops.append(self._current_loop)
            self._current_loop = None
            self._message_agent_thought = None
        elif not self._current_loop and self._agent_loops:
            self._agent_loops[-1].status = 'agent_finish'