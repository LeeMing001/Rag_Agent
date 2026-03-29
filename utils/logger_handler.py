import logging # 专门用于记录日志的模块
from utils.path_tool import get_abs_path
import os
from datetime import datetime
# 日志文件目录
LOG_ROOT=get_abs_path('logs')
# 确保日志目录存在
os.makedirs(LOG_ROOT,exist_ok=True)
# 日志格式的配置 error info debug
DEFAULT_LOG_FORMAT=logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
def get_logger(
        name:str="agent",
        console_level:int=logging.INFO,
        file_level:int=logging.DEBUG,
        log_file=None
)->logging.Logger:
    logger=logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    # 控制台日志
    console_handler=logging.StreamHandler()  # 处理器
    console_handler.setLevel(console_level)  # 控制台只显示该级别以上的内容
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)
    # 文件日志
    if not log_file:
        log_file=os.path.join(LOG_ROOT,f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)
    return logger
logger=get_logger()

if __name__ == '__main__':
    logger.info("信息日志")
    logger.error("错误日志")
    logger.debug("调试日志")
    logger.warning("警告日志")