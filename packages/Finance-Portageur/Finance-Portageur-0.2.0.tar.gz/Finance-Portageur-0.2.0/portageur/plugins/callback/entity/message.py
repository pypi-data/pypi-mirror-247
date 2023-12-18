import enum
from typing import Any, cast, Union, List
from langchain.schema import HumanMessage, AIMessage, SystemMessage, BaseMessage, FunctionMessage
from pydantic import BaseModel


class LLMMessage(BaseModel):
    prompt: str = ''
    prompt_tokens: int = 0
    completion: str = ''
    completion_tokens: int = 0

class PromptMessageFileType(enum.Enum):
    IMAGE = 'image'

    @staticmethod
    def value_of(value):
        for member in PromptMessageFileType:
            if member.value == value:
                return member
        raise ValueError(f"No matching enum found for value '{value}'")

class MessageType(enum.Enum):
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'

class PromptMessageFile(BaseModel):
    type: PromptMessageFileType
    data: Any


class ImagePromptMessageFile(PromptMessageFile):
    class DETAIL(enum.Enum):
        LOW = 'low'
        HIGH = 'high'

    type: PromptMessageFileType = PromptMessageFileType.IMAGE
    detail: DETAIL = DETAIL.LOW


class LCHumanMessageWithFiles(HumanMessage):
    # content: Union[str, List[Union[str, Dict]]]
    content: str
    files: list[PromptMessageFile]

class PromptMessage(BaseModel):
    type: MessageType = MessageType.USER
    content: str = ''
    files: list[PromptMessageFile] = []
    function_call: dict = None


def to_prompt_messages(messages: list[BaseMessage]):
    prompt_messages = []
    for message in messages:
        if isinstance(message, HumanMessage):
            if isinstance(message, LCHumanMessageWithFiles):
                prompt_messages.append(PromptMessage(
                    content=message.content,
                    type=MessageType.USER,
                    files=message.files
                ))
            else:
                prompt_messages.append(
                    PromptMessage(
                        content=message.content, type=MessageType.USER))
                
        elif isinstance(message, AIMessage):
            message_kwargs = {
                'content': message.content,
                'type': MessageType.ASSISTANT
            }

            if 'function_call' in message.additional_kwargs:
                message_kwargs['function_call'] = message.additional_kwargs['function_call']

            prompt_messages.append(PromptMessage(**message_kwargs))

        elif isinstance(message, SystemMessage):
            prompt_messages.append(PromptMessage(content=message.content, type=MessageType.SYSTEM))
        elif isinstance(message, FunctionMessage):
            prompt_messages.append(PromptMessage(content=message.content, type=MessageType.USER))
    return prompt_messages