import os
import glob
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.vectorstore import VECTOR_STORE, drop_collection 
from src.util import pad_fields, rename_fields

# === Load PDFs ===
pdf_files = glob.glob("data/*.pdf")
pdf_docs = [PyPDFLoader(file).load()[0] for file in pdf_files]
print(f"✅ Loaded {len(pdf_docs)} PDF docs")

# === Load web URLs ===
URL_FILE = "data/web_urls.txt"
web_urls = open(URL_FILE).readlines()
web_urls = [url.strip() for url in web_urls if url.strip()]
web_docs = WebBaseLoader(web_paths=web_urls).load()
print(f"✅ Loaded {len(web_docs)} web docs")

#web_docs = []

# === Load preprocessed .txt files ===
text_docs = []
txt_folder = "docs"
for file in os.listdir(txt_folder):
    if file.endswith(".txt"):
        loader = TextLoader(os.path.join(txt_folder, file))
        text_docs.extend(loader.load())
print(f"✅ Loaded {len(text_docs)} plain text docs")

# === Combine all docs ===
all_docs = pdf_docs + web_docs + text_docs
pad_fields(all_docs)
rename_fields(all_docs)
print(f"📦 Total loaded docs: {len(all_docs)}")

# === Chunk them ===
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(all_docs)
print(f"✂️ Split into {len(chunks)} chunks")

# === Store in vector DB ===
drop_collection()
added = VECTOR_STORE.add_documents(chunks)
print(f"📥 Added {len(added)} chunks to vector store")
