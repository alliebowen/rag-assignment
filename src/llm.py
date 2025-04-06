from langchain.chat_models import init_chat_model

_API_KEY = "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"
_MODEL = "gpt-4o-mini"

LLM = init_chat_model(model=_MODEL, model_provider="openai", api_key=_API_KEY)