from typing import Any, Dict, List, Optional
from uuid import UUID
import enum,pdb
from langchain.schema import LLMResult, BaseMessage
from langchain.callbacks.base import BaseCallbackHandler
from portageur.plugins.callback.entity.message import *
from portageur.kdutils.exception import ConversationTaskStoppedException,ConversationTaskInterruptException
from portageur.kdutils.logger import kd_logger

class LLMCallbackHandler(BaseCallbackHandler):
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.llm_message = LLMMessage()
        self.start_at = None
        #self.conversation_message_task = conversation_message_task

        #self.output_moderation_handler = None

    #def init_output_moderation(self):
    #    app_model_config = self.conversation_message_task.app_model_config
        
    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True
    
    def on_chat_model_start(self, serialized: Dict[str, Any],
                            messages: List[List[BaseMessage]],
                            **kwargs: Any):
        real_prompts = []
        for message in messages[0]:
            if message.type == MessageType.USER:
                role = 'user'
            elif message.type == MessageType.ASSISTANT:
                role = 'assistant'
            else:
                role = 'system'
        
        real_prompts.append({
                "role": role,
                "text": message.content,
                "files": [{
                    "type": file.type.value,
                    "data": file.data[:10] + '...[TRUNCATED]...' + file.data[-10:],
                    "detail": file.detail.value if isinstance(file, ImagePromptMessageFile) else None,
                } for file in (message.files if isinstance(message, LCHumanMessageWithFiles) else [])]
            })
        self.llm_message.prompt = real_prompts
        self.llm_message.prompt_tokens = self.model_instance.get_num_tokens(to_prompt_messages(messages[0]))

    def on_llm_start(self, serialized: Dict[str, Any], 
                     prompts: List[str], **kwargs: Any):
        pdb.set_trace()
        self.llm_message.prompt_tokens = self.model_instance.get_num_tokens(
            [PromptMessage(content=prompts[0])])

    def on_llm_end(self, response: LLMResult, **kwargs: Any):
        self.llm_message.completion = response.generations[0][0].text
        if response.llm_output and 'token_usage' in response.llm_output:
            if 'prompt_tokens' in response.llm_output['token_usage']:
                self.llm_message.prompt_tokens = response.llm_output['token_usage']['prompt_tokens']

            if 'completion_tokens' in response.llm_output['token_usage']:
                self.llm_message.completion_tokens = response.llm_output['token_usage']['completion_tokens']
            else:
                self.llm_message.completion_tokens = self.model_instance.get_num_tokens(
                    [PromptMessage(content=self.llm_message.completion)])
                
        else:
            self.llm_message.completion_tokens = self.model_instance.get_num_tokens(
                [PromptMessage(content=self.llm_message.completion)])
        

    def on_llm_new_token(self, token: str, **kwargs: Any):
        try:
            self.llm_message.completion += token
        except ConversationTaskStoppedException as ex:
            self.on_llm_error(error=ex)
            raise ex
        
    def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        if isinstance(error, ConversationTaskStoppedException):
                self.llm_message.completion_tokens = self.model_instance.get_num_tokens(
                    [PromptMessage(content=self.llm_message.completion)]
                )
        if isinstance(error, ConversationTaskInterruptException):
            self.llm_message.completion_tokens = self.model_instance.get_num_tokens(
                [PromptMessage(content=self.llm_message.completion)]
            )
        else:
            kd_logger.debug("on_llm_error: %s", error)