from langchain.chat_models import init_chat_model

_API_KEY = ""
_MODEL = "gpt-4o-mini"

LLM = init_chat_model(model=_MODEL, model_provider="openai", api_key=_API_KEY)