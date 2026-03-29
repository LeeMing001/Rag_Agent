# Rag_Agent

# 智扫机器人智能客服系统

基于 LangChain + RAG 技术的扫地机器人智能问答系统，支持向量检索、智能总结和报告生成功能。

## 🌟 项目特色

- **RAG 检索增强生成**：基于 ChromaDB 向量数据库，精准检索专业知识
- **ReAct 代理框架**：支持多工具调用和智能决策
- **流式输出**：实时显示回答，提升用户体验
- **动态提示词切换**：根据场景自动切换普通问答/报告生成模式
- **知识库去重**：基于 MD5 的文件去重机制，避免重复加载

## 🏗️ 项目结构

PythonAgent/ 
├── agent/ # Agent 相关模块 
│ ├── react_agent.py # ReAct 代理主类 
│ └── tools/ # 工具和中间件 
│ ├── agent_tools.py # 工具函数定义 
│ └── middleware.py # 中间件（日志、提示词切换） 
├── config/ # 配置文件 
│ ├── agent.yml # Agent 配置 
│ ├── chroma.yml # 向量数据库配置 
│ ├── prompts.yml # 提示词路径配置 
│ └── rag.yml # RAG 配置 
├── data/ # 知识库数据 
│ ├── external/ # 外部数据（CSV 等）
│ ├── 扫地机器人100问.pdf 
│ ├── 扫拖一体机器人100问.txt 
│ ├── 故障排除.txt 
│ ├── 维护保养.txt 
│ └── 选购指南.txt 
├── model/ # 模型工厂 
│ └── factory.py # ChatModel 和 Embedding 工厂 
├── rag/ # RAG 核心模块 
│ ├── rag_service.py # RAG 总结服务 
│ └── vector_store.py # 向量存储服务 
├── utils/ # 工具类 
│ ├── config_handler.py # YAML 配置加载 
│ ├── file_handler.py # 文件处理（PDF/TXT） 
│ ├── logger_handler.py # 日志处理 
│ ├── path_tool.py # 路径工具 
│ └── prompt_loader.py # 提示词加载 
├── app.py # Streamlit Web 界面 
└── requirements.txt # 依赖包列表

## 🚀 快速开始

### 环境要求

- Python 3.13+
- macOS / Linux / Windows

### 安装步骤

1. **克隆项目**
2. **创建并激活虚拟环境**
3. **安装依赖**
4. **初始化向量知识库**
5. **启动 Web 界面**
## ⚙️ 配置说明

### 环境变量配置

在项目根目录创建 `.env` 文件：

### 核心配置文件

**config/chroma.yml** - 向量数据库配置

## 🛠️ 核心功能

### 1. 智能问答

用户提问 → 向量检索 → 总结回答

### 2. 工具调用

支持多种工具：
- `rag_summarize`: 向量检索专业知识
- `get_weather`: 查询天气
- `get_location`: 获取用户位置
- `get_user_record`: 查询用户记录
- `fill_context`: 触发报告生成模式

### 3. 报告生成

通过中间件动态切换提示词：
调用 fill_context 工具触发报告模式
agent.execute_stream("给我生成我的使用报告")

## 🔧 开发指南

### 添加新工具
在 `agent/tools/agent_tools.py` 中添加：
@tool(description="工具描述") def new_tool(param: str) -> str: """工具文档字符串""" return f"处理结果：{param}"
然后在 `react_agent.py` 中注册：

### 添加中间件

在 `agent/tools/middleware.py` 中定义：
@before_model def custom_middleware(state: AgentState, runtime: Runtime): # 自定义逻辑 return None
在 `react_agent.py` 中注册：
middleware=[..., custom_middleware]
## 📊 性能优化

### 向量检索优化

1. **调整 chunk_size**：根据文档类型调整分块大小（建议 300-800）
2. **设置 score_threshold**：过滤低相似度结果（建议 0.3-0.5）
3. **使用高质量 Embedding 模型**：如 Qwen3-Embedding

### Token 消耗优化

1. **精简参考资料**：设置合理的 `k` 值（3-5）
2. **优化提示词**：移除冗余描述
3. **使用缓存**：避免重复问题检索

## 🐛 常见问题

### Q: 向量库加载失败？
A: 检查 `data/` 目录下是否有有效的 `.txt` 或 `.pdf` 文件

### Q: 检索结果为空？
A: 
1. 运行 `python rag/vector_store.py` 重新加载知识库
2. 降低 `score_threshold` 阈值
3. 增大 `k` 值

### Q: Streamlit 启动失败？
A: 
source .venv/bin/activate python -m streamlit run app.py

## 📝 更新日志

- **v1.0.0** (2026-03)
  - 初始版本发布
  - 支持基础 RAG 问答
  - 实现动态提示词切换
  - 集成 Streamlit Web 界面

## 📄 License

MIT License

## 👥 作者

liming

---

**注意**：首次使用前必须先执行 `python rag/vector_store.py` 初始化知识库！

