"""
yaml
k:v
"""
"""
4个不同的配置文件：
1.rag
2.向量数据库
3.prompts
4.agent

"""
import yaml
from utils.path_tool import get_abs_path

def load_rag_config(config_path:str=get_abs_path("config/rag.yml"),encoding:str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config
def load_vector_config(config_path:str=get_abs_path("config/chroma.yml"),encode="utf-8"):
    with open(config_path, "r", encoding=encode) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config
def load_prompt_config(config_path:str=get_abs_path("config/prompts.yml"),encode="utf-8"):
    with open(config_path, "r", encoding=encode) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config
def load_agent_config(config_path:str=get_abs_path("config/agent.yml"),encode="utf-8"):
    with open(config_path, "r", encoding=encode) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config
rag_config=load_rag_config()
vector_config=load_vector_config()
prompt_config=load_prompt_config()
agent_config=load_agent_config()
if __name__ == '__main__':
   print( rag_config["chat_model_name"])
