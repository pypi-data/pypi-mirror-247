from langchain.agents import initialize_agent, AgentType
from portageur.plugins.agents.tools import create_tools


def create_executor(model, tools, agent_kwargs,
                    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, memory=None, max_iterations=10):
    return initialize_agent(
        [tool.to_tool() for tool in create_tools(tools)], model.instance(),
        agent=agent,
        verbose=True, agent_kwargs=agent_kwargs, handle_parsing_errors=True,
        memory=memory, max_iterations=max_iterations)
