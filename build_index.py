# build_index.py
import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

docs_path = Path("docs")
filepaths = list(docs_path.glob("*.txt"))
if not filepaths:
    raise FileNotFoundError("No .txt files found.")

all_documents = []
for path in filepaths:
    loader = TextLoader(str(path), encoding="utf-8")
    all_documents.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(all_documents)

embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(split_docs, embedding)
vectorstore.save_local("faiss_index")

print("✅ Index built and saved to 'faiss_index/'")
