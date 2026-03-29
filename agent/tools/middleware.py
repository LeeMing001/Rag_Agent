from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain_core.messages import ToolMessage
from langchain_core.messages.content import ToolCall
from langgraph.prebuilt.tool_node import ToolCallRequest
from utils.prompt_loader import load_system_prompt,  load_report_prompt
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger
from typing import Callable
@wrap_tool_call
def monitor_tool(
        request:ToolCallRequest,# 请求的数据
        handler:Callable[[ToolCallRequest],ToolMessage|Command],# 函数
)->ToolMessage|Command:
    logger.info(f"[monitor_tool]请求工具:{request.tool_call['name']}")
    logger.info(f"[monitor_tool]请求工具:{request.tool_call['args']}")
    try:
        res= handler(request)
        logger.info(f"[monitor_tool]工具返回:{res}")
        if request.tool_call['name']=="fill_context_for_report":
            request.runtime.context["report"]=True
        return res
    except Command as e:
        logger.info(f"[monitor_tool]工具返回:{e}")
        return e
    except Exception as e:
        logger.error(f"[monitor_tool]工具执行错误:{e}")
        raise e
@before_model
def log_before_model(
        state:AgentState,
        runtime:Runtime
):
    logger.info(f"[log_before_model]即将调用模型,带有{len(state['messages'])}")
    logger.debug(f"[log_before_model]{type(state['messages'])}|{state['messages'][-1].content.strip()}")
    return None


@dynamic_prompt  #每次在生成提示词之前，调用此函数
def report_prompt_switch(request:ModelRequest):
    is_report=request.runtime.context.get("report",False)
    if is_report:
        return load_report_prompt()
    return load_system_prompt()