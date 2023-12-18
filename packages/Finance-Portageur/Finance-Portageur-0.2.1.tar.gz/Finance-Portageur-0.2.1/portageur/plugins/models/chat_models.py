# -*- coding: utf-8 -*-
import pdb
from portageur.plugins.models.base import create_model_base
from langchain.chat_models import AzureChatOpenAI as AzureChatOpenAIImpl
from langchain.chat_models import ChatOpenAI as ChatOpenAIImpl
from langchain.chat_models import ChatGooglePalm as ChatGooglePalmImpl
from langchain.schema import BaseMessage, ChatMessage, HumanMessage, AIMessage, SystemMessage, FunctionMessage
from langchain.chat_models.openai import _import_tiktoken,convert_message_to_dict

class AzureChatOpenAI(create_model_base('chat_models')):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.impl = AzureChatOpenAIImpl(**kwargs)
        self.provider_name = "azure_openai"
        self.model_name = kwargs['model_name']

    def get_num_tokens(self, messages):
        return super().get_num_tokens(model_name=self.model_name, 
                                      convert_class=convert_message_to_dict,
                                      tiktoken_class=_import_tiktoken,
                                      messages=messages)

    def save(self):
        return super().save()


class ChatOpenAI(create_model_base('chat_models')):

    def __init__(self, **kwargs):
        super().__init__()
        self.impl = ChatOpenAIImpl(**kwargs)

    def save(self):
        return super().save()


class ChatGooglePalm(create_model_base('chat_models')):

    def __init__(self, **kwargs):
        super().__init__()
        self.impl = ChatGooglePalm(**kwargs)

    def save(self):
        return super().save()
