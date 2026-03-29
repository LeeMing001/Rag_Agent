from utils.config_handler import prompt_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

def load_system_prompt():
    try:
        system_prompt_path=get_abs_path(prompt_config["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompt]在yaml配置项中没有找到main_prompt_path字段")
    try:
        return open(system_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompt]解析系统提示词出错，{str(e)}")
        raise(e)
def load_rag_prompt():
    try:
        rag_prompt_path=get_abs_path(prompt_config["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_summarize_prompt]在yaml配置项中没有找到rag_summarize_prompt_path字段")
    try:
        return open(rag_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompt]解析rag提示词出错，{str(e)}")
        raise (e)
def load_report_prompt():
    try:
        report_prompt_path=get_abs_path(prompt_config["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompt]在yaml配置项中没有找到report_prompt_path字段")
    try:
        return open(report_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompt]解析报告提示词出错，{str(e)}")
        raise (e)
if __name__ == '__main__':
    # print(load_system_prompt())
    # print(load_rag_prompt())
    print(load_report_prompt())