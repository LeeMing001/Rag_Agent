import os.path
from utils.path_tool import get_abs_path
from langchain_core.documents import Document
from langchain_chroma import Chroma
from utils.config_handler import vector_config
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger

import os
import dotenv
dotenv.load_dotenv()
os.environ["OPENAI_API_BASE"]=vector_config["api_base"]
os.environ["OPENAI_API_KEY"]=vector_config["api_key"]

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=vector_config["collection_name"],
            embedding_function=embed_model,
            persist_directory=vector_config["persist_directory"]
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=vector_config["chunk_size"],
            chunk_overlap=vector_config["chunk_overlap"],
            separators=vector_config["separators"],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": vector_config["k"]})

    def load_documents(self):
        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(vector_config["md5_hex_store"])):
                open(get_abs_path(vector_config["md5_hex_store"]), "w", encoding="utf-8").close()
                return False
            with open(get_abs_path(vector_config["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
            return False

        def save_md5_hex(md5_for_save: str):
            with open(get_abs_path(vector_config["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_save)
                f.write("\n")

        def get_file_documents(read_path: str):
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            elif read_path.endswith(".txt"):
                return txt_loader(read_path)
            else:
                logger.error(f"[get_file_documents]不支持的文件类型:{read_path}")
                return []

        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(vector_config["data_path"]),
            tuple(vector_config["allow_knowledge_file_type"])
        )
        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if not md5_hex:
                logger.error(f"[load_documents]获取文件md5失败:{path}")
                continue
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue

                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue

                # 将内容存入向量库
                self.vector_store.add_documents(split_document)

                # 记录这个已经处理好的文件的md5，避免下次重复加载
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path} 内容加载成功")
            except Exception as e:
                # exc_info为True会记录详细的报错堆栈，如果为False仅记录报错信息本身
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}", exc_info=True)
                continue



if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_documents()
    retriever=vs.get_retriever()
    res=retriever.invoke("维修")
    for r in res:
        print(r.page_content)
        print('-'*20)

