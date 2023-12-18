# -*- coding: utf-8 -*-
from portageur.plugins.models.base import create_model_base
from langchain.embeddings.openai import OpenAIEmbeddings as OpenAIEmbeddingsImpl


class OpenAIEmbeddings(create_model_base('chat_models')):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.impl = OpenAIEmbeddingsImpl(**kwargs)

    def save(self):
        return super().save()
