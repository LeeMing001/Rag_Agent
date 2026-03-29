
"""
总结服务：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompt
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model

def print_prompt(prompt):
    print('\n' + '=' * 60)
    print('Prompt 内容:')
    print('=' * 60)
    prompt_str = str(prompt) if not isinstance(prompt, str) else prompt
    print(prompt_str)  # 直接打印，不要用 repr()
    print('=' * 60 + '\n')
    return prompt



class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.vector_store.load_documents()   # 这句可以单独做一个面向企业端的信息上传服务
        self.retriever=self.vector_store.get_retriever()
        self.rag_prompt=load_rag_prompt()
        self.prompt_template=PromptTemplate.from_template(self.rag_prompt)
        self.model=chat_model
        self.chain=self._init_chain()
    def _init_chain(self):
        chain=self.prompt_template|print_prompt|self.model|StrOutputParser()
        return chain
    def retriever_docs(self,query:str)->list[Document]:
        return self.retriever.invoke(query)
    def rag_summarize(self,query:str)->str:
        context_docs=self.retriever_docs(query)
        context=''
        counter=0
        for doc in context_docs:
            counter+=1
            context+=f"[参考资料{counter}]:{doc.page_content}|[参考资料元数据]:{doc.metadata}\n\n"
        return self.chain.invoke(
            {
                "input":query,
                "context":context
            }
        )
if __name__ == '__main__':
    rag=RagSummarizeService()
    res=rag.rag_summarize("机器人找不到充电座怎么处理")
    print(res)