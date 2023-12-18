# -*- coding: utf-8 -*-
import importlib, abc, warnings, arrow, copy, pdb, enum
from packaging.version import parse as LooseVersion
from langchain import __version__
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from portageur.kdutils.code import encode, decode
from portageur.plugins.callback.entity.message import *


class ModelBase():

    def __init__(self, **kwargs):
        self.impl = None
        self.provider_name = None
        self.kwargs = copy.deepcopy(kwargs)
        self.update_time = arrow.now().format("YYYY-MM-DD HH:mm:ss")


    def get_num_tokens(self, model_name, convert_class, tiktoken_class, messages):
        """
        get num tokens of prompt messages.

        :param messages:
        :return:
        """
        ### 消息转化
        lc_messages = []
        for message in messages:
            if message.type == MessageType.USER:
                lc_messages.append(HumanMessage(content=message.content))
            elif message.type == MessageType.ASSISTANT:
                additional_kwargs = {}
                if message.function_call:
                    additional_kwargs['function_call'] = message.function_call
                lc_messages.append(AIMessage(content=message.content, additional_kwargs=additional_kwargs))
            elif message.type == MessageType.SYSTEM:
                lc_messages.append(SystemMessage(content=message.content))

        if self.provider_name == "azure_openai":
            model_name = model_name.replace("gpt-35", "gpt-3.5")
        
        tiktoken_ = tiktoken_class()
        try:
            encoding = tiktoken_.get_encoding(model_name)
        except:
            encoding = tiktoken_.get_encoding("cl100k_base")

        if model_name.startswith("gpt-3.5-turbo"):
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            tokens_per_message = 4
            # if there's a name, the role is omitted
            tokens_per_name = -1
        elif model_name.startswith("gpt-4"):
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(
                f"get_num_tokens_from_messages() is not presently implemented "
                f"for model {model_name}."
                "See https://github.com/openai/openai-python/blob/main/chatml.md for "
                "information on how messages are converted to tokens."
            )
        num_tokens = 0
        for m in lc_messages:
            message = convert_class(m)
            num_tokens += tokens_per_message
            for key, value in message.items():
                if key == "function_call":
                    for f_key, f_value in value.items():
                        num_tokens += len(encoding.encode(f_key))
                        num_tokens += len(encoding.encode(f_value))
                else:
                    num_tokens += len(encoding.encode(value))

                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3
        return num_tokens


    def predict(self, **kwargs):
        return self.impl.predict_messages(**kwargs)

    async def apredict(self, immed=True, **kwargs):
        return await self.impl.apredict_messages(**kwargs) if immed else self.impl.predict_messages(**kwargs)

    @abc.abstractmethod
    def save(self):
        if self.__class__.__module__ == '__main__':
            warnings.warn(
                "model is defined in a main module. The model_name may not be correct."
            )
        model_desc = dict(model_name=self.__class__.__module__ + "." +
                          self.__class__.__name__,
                          language='python',
                          update_time=self.update_time,
                          kwargs=encode(self.kwargs),
                          impl=encode(self.impl),
                          internal_model=self.impl.__class__.__module__ + "." +
                          self.impl.__class__.__name__)
        return model_desc

    @classmethod
    @abc.abstractmethod
    def load(cls, model_desc):
        layout = cls()
        layout.update_time = model_desc['update_time']
        layout.kwargs = decode(model_desc['kwargs'])
        layout.impl = decode(model_desc['impl'])
        return model_desc

    @property
    def m(self):
        return self.impl


def create_model_base(party_name=None):
    if not party_name:
        return ModelBase
    else:

        class ExternalLibBase(ModelBase):
            _lib_name = party_name

            def save(self) -> dict:
                model_desc = super().save()
                if self._lib_name == 'chat_models':
                    model_desc[self._lib_name + "_version"] = __version__
                elif self._lib_name == 'llms':
                    model_desc[self._lib_name + "_version"] = __version__
                elif self._lib_name == 'embedding':
                    model_desc[self._lib_name + "_version"] = __version__
                else:
                    raise ValueError(
                        "3rd party lib name ({0}) is not recognized".format(
                            self._lib_name))
                return model_desc

            @classmethod
            def load(cls, model_desc):
                obj_layout = super().load(model_desc)
                if cls._lib_name == 'chat_models':
                    current_version = __version__
                elif cls._lib_name == 'llms':
                    current_version = __version__
                elif cls._lib_name == 'embedding':
                    current_version = __version__
                else:
                    raise ValueError(
                        "3rd party lib name ({0}) is not recognized".format(
                            cls._lib_name))
                if LooseVersion(current_version) < LooseVersion(
                        model_desc[cls._lib_name + "_version"]):
                    warnings.warn(
                        'Current {2} version {0} is lower than the model version {1}. '
                        'Loaded model may work incorrectly.'.format(
                            __version__, model_desc[cls._lib_name],
                            cls._lib_name))
                return obj_layout

        return ExternalLibBase


def create_models(name):
    return importlib.import_module('langchain.chat_models').__getattribute__(
        name)


def create_llms(name):
    return importlib.import_module('langchain.llms').__getattribute__(name)

def create_embedding(name):
    return importlib.import_module('langchain.embedding').__getattribute__(name)
