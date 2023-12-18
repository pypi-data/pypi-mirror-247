from __future__ import annotations

from typing import Union

from langchain.agents import AgentOutputParser
from langchain.output_parsers.json import parse_json_markdown
from langchain.schema import AgentAction, AgentFinish, OutputParserException
from portageur.plugins.prompt.qa_memory import QAHint


# Define a class that parses output for conversational agents
class ConvoOutputParser(AgentOutputParser):
    """Output parser for the conversational agent."""

    def get_format_instructions(self) -> str:
        """Returns formatting instructions for the given output parser."""
        return QAHint.output_parser_format_instruction()

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        """Attempts to parse the given text into an AgentAction or AgentFinish.

        Raises:
             OutputParserException if parsing fails.
        """
        try:
            # Attempt to parse the text into a structured format (assumed to be JSON
            # stored as markdown)
            response = parse_json_markdown(text)

            # If the response contains an 'action' and 'action_input'
            if "action" in response and "action_input" in response:
                action, action_input = response["action"], response["action_input"]

                # If the action indicates a final answer, return an AgentFinish
                if action == "Final Answer":
                    return_values = {"output": action_input}
                    # the title of the current thread
                    if 'chat_title' in response:
                        return_values['title'] = response["chat_title"]
                    # the suggestions of the next round of questions
                    if 'suggestions' in response:
                        return_values['suggestions'] = response["suggestions"]

                    return AgentFinish(return_values, text)
                else:
                    # Otherwise, return an AgentAction with the specified action and
                    # input
                    return AgentAction(action, action_input, text)
            else:
                # If the necessary keys aren't present in the response, raise an
                # exception
                raise OutputParserException(
                    f"Missing 'action' or 'action_input' in LLM output: {text}"
                )
        except Exception as e:
            # If any other exception is raised during parsing, also raise an
            # OutputParserException
            raise OutputParserException(f"Could not parse LLM output: {text}") from e

    @property
    def _type(self) -> str:
        return "conversational_chat"
