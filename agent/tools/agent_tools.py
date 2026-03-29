import csv
import os.path

from langchain_core.tools import tool

from rag.rag_service import RagSummarizeService
import random

from utils.config_handler import agent_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

rag = RagSummarizeService()
user_id = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
mouth_arr=["2025-01", "2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08"]

@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)


@tool(description="查询指定城市的天气情况")
def get_weather(city: str) -> str:
    return f"{city}天气晴朗，温度26摄氏度，南风1级，湿度50%"


@tool(description="获取用户位置,以纯字符串返回")
def get_location() -> str:
    return "上海"


@tool(description="获取用户ID,以纯字符串返回")
def get_user_id() -> str:
    return random.choice(user_id)
@tool(description="获取当前月份")
def get_month() -> str:
    return random.choice(mouth_arr)

external_data={}
def generate_external_data():
    """
    {
    "user_id":{
        "month":{
            "特征":
            "效率":
            …
        },
        "month":{
            "特征":
            "效率":
            …
        }
    }
    :return:
    """
    if not external_data:
        external_data_path=get_abs_path(agent_config["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"[generate_external_data]外部数据文件不存在:{external_data_path}")
        with open(external_data_path,"r",encoding="utf-8") as f:
            reader=csv.reader(f)
            header=next(reader,None)
            if header is None:
                return #空文件
            for row in reader:
                if len(row)<6:
                    continue
                user_id=row[0].strip('"')
                feature=row[1].strip('"')
                efficiency=row[2].strip('"')
                consumables = row[3].strip('"')
                comparison = row[4].strip('"')
                time = row[5].strip('"')
                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(description="获取当前用户当前月份的使用记录，以纯字符串返回，如果未检索到，返回空字符串")
def get_user_record(user_id: str,month: str) -> str:
    generate_external_data()
    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[get_user_record]未检索到用户{user_id}的{month}使用记录")
        return ""

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文，为后续提示词切换提供上下文信息")
def fill_context():
    return "已调用"
if __name__ == '__main__':
    r=get_user_record("1021","2025-03")
    print(r)

