from langchain.vectorstores import Milvus
from langchain.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/quora-distilbert-multilingual")

VECTOR_STORE = Milvus(
    embedding_function=embedding,
    collection_name="rag_documents",
    connection_args={"host": "localhost", "port": "19530"}
)

def drop_collection():
    VECTOR_STORE.drop()

def pad_fields(docs):
    for doc in docs:
        if "source" not in doc.metadata:
            doc.metadata["source"] = "unknown"

def rename_fields(docs):
    for doc in docs:
        if "title" in doc.metadata:
            doc.metadata["source_title"] = doc.metadata.pop("title")
