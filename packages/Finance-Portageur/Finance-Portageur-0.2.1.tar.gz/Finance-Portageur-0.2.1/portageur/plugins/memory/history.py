import json
import logging
from typing import List

from langchain.schema import (
    BaseChatMessageHistory,
)
from langchain.schema.messages import BaseMessage, _message_to_dict, messages_from_dict
from langchain.pydantic_v1 import BaseModel, Field

DEFAULT_DBNAME = "chat_history"
DEFAULT_COLLECTION_NAME = "message_store"

class SimpleChatMessageHistory(BaseChatMessageHistory):
    """Chat message history that stores history.
    """

    def __init__(
        self,
        session_id: str,
    ):
        self.session_id = session_id
        self.history_messages = []
        return

    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the list"""
        self.history_messages.append(message)

    def clear(self) -> None:
        """Clear the chat history"""
        self.history_messages = []

    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        return self.history_messages

    def serialize(self) -> List:
        serialized_messages = [json.dumps(_message_to_dict(message)) for message in self.history_messages]
        return serialized_messages

    def restore(self, serialized_messages: List) -> None:
        self.history_messages = messages_from_dict([json.loads(message) for message in serialized_messages])