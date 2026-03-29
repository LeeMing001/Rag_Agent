"""文件处理工具"""
import os.path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader

import os,hashlib
from utils.logger_handler import logger
def get_file_md5_hex(file_path):
    if not os.path.exists(file_path):
         logger.error(f"[md5计算]文件不存在:{file_path}")
    if not os.path.isfile(file_path):
         logger.error(f"[md5计算]不是文件:{file_path}")
    md5_obj = hashlib.md5()
    chunk_size = 4096
    try:
        with open(file_path, 'rb') as f: # 2进制方式读取
            while chunk:=f.read(chunk_size):
                md5_obj.update(chunk)
            """
            chunk=f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)
                chunk=f.read(chunk_size)
            """
            md5_hex=md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"获取文件md5失败:{file_path}")
        return None
def listdir_with_allowed_type(path:str,allowed_types:tuple[str]): #返回文件夹中的文件列表（允许的文件后缀）
    files=[]
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]参数path不是文件夹:{path}")
        return files
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path,f))
    return tuple(files)

def pdf_loader(filepath:str,password:str=None)->list[Document]:
    return PyPDFLoader(filepath,password).load()
def txt_loader(filepath:str)->list[Document]:
    return TextLoader(filepath).load()