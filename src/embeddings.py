from langchain_openai import OpenAIEmbeddings

_API_KEY = "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"
_MODEL = "text-embedding-3-large"

EMBEDDINGS = OpenAIEmbeddings(model=_MODEL, api_key=_API_KEY)