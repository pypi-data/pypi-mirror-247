import yaml,os,copy
from dataclasses import dataclass
from plugins.auth.base import BaseAuth, ChatModelManager, BasicModel
from portageur.plugins.models.chat_models import ChatOpenAI as ChatOpenAIImpl
from portageur.plugins.models.embeddings import OpenAIEmbeddings as OpenAIEmbeddingsImpl

@dataclass
class OpenAIAuth(BaseAuth):
    auth_index: int
    api_key: str
    api_base: str


class OpenAIChatManager(ChatModelManager):
    endpoints = {
        'completions': 'https://api.openai.com/v1/completions',
        'embeddings': 'https://api.openai.com/v1/embeddings',
        'chat_completions': 'https://api.openai.com/v1/chat/completions'
    }
    name = 'openai'

    def __init__(self, config_path):
        self.auth_config(config_path=config_path)

    def auth_config(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        openai_config = config.get('openai', {})
        self.auths = super(OpenAIChatManager,
                           self).auth_config(openai_config, OpenAIAuth)

model_manager = OpenAIChatManager(config_path=os.environ['USER_FILE'])

class ChatOpenAI(BasicModel):

    def __init__(self, **kwargs):
        super(ChatOpenAI,self).__init__(ChatOpenAIImpl, model_manager, **kwargs)

class OpenAIEmbeddings(BasicModel):

    def __init__(self, **kwargs):
        super(OpenAIEmbeddings,self).__init__(OpenAIEmbeddingsImpl, model_manager, **kwargs)