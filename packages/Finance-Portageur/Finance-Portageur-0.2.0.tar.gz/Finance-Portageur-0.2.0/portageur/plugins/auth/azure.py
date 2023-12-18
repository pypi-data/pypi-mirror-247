import yaml, copy, six, pdb, os
from dataclasses import dataclass
#from seleya import *
#from seleya.Toolset import blob_service
from portageur.kdutils.singleton import Singleton
from portageur.plugins.auth.base import BaseAuth, ModelManager, ChatModelManager,BasicModel
from portageur.plugins.models.chat_models import AzureChatOpenAI as AzureChatOpenAIImpl
from portageur.plugins.models.embeddings import OpenAIEmbeddings as OpenAIEmbeddingsImpl


@dataclass
class AzureOpenAIAuth(BaseAuth):
    auth_index: int = 0
    api_key: str = ''
    api_base: str = ''
    api_version: str = ''
    api_type: str = ''


@six.add_metaclass(Singleton)
class AzureOpenAIManager(ModelManager):
    name = 'azureai'

    def __init__(self, config_path):
        self.auth_config(config_path=config_path)

    def auth_config(self, config_path):
        if not os.path.exists(config_path):
            '''
            SeleyaAPI.login(username=os.environ['seleya_username'],
                            password=os.environ['seleya_password'])
            blob_service.BlobService().download_file(
                container_name='data',
                remote_file_name=os.path.join("molecule", "config.yml"),
                local_file_name=config_path)
            '''
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        openai_config = config.get('azureopenai', {})
        self.auths = super(AzureOpenAIManager,
                           self).auth_config(openai_config, AzureOpenAIAuth)

model_manager = AzureOpenAIManager(config_path=os.environ['USER_FILE'])

class AzureChatOpenAI(BasicModel):

    def __init__(self, **kwargs):
        super(AzureChatOpenAI,self).__init__(AzureChatOpenAIImpl, model_manager, **kwargs)

class OpenAIEmbeddings(BasicModel):

    def __init__(self, **kwargs):
        super(OpenAIEmbeddings,self).__init__(OpenAIEmbeddingsImpl, model_manager, **kwargs)