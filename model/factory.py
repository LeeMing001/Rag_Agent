
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from typing import Optional
from utils.config_handler import vector_config
from abc import ABC,abstractmethod
import os
os.environ["OPENAI_API_BASE"]=vector_config["api_base"]
os.environ["OPENAI_API_KEY"]=vector_config["api_key"]
class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self)->Optional[Embeddings|BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self)->Optional[Embeddings|BaseChatModel]:
        return ChatOpenAI(model_name=vector_config["chat_model_name"])

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) ->Optional[Embeddings|BaseChatModel]:
        return OpenAIEmbeddings(model=vector_config["embedding_model_name"])

chat_model=ChatModelFactory().generator()
embed_model=EmbeddingsFactory().generator()