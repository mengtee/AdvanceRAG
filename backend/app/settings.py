import os
from typing import Dict
from llama_index.core.settings import Settings
from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.together import TogetherEmbedding


def llm_config_from_env() -> Dict:
    from llama_index.core.constants import DEFAULT_TEMPERATURE
    #MODEL
    model = "mistralai/Mixtral-8x7B-Instruct-v0.1" #os.getenv("MODEL")
    TOGETHER_API_KEY = "e3e0d37084a3f9a9d2ffd9f8f834faec3ed5e65c92d0ab81f4971ff505c3a306"# os.getenv("TOGETHER_API_KEY")
    temperature = os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)
    max_tokens = os.getenv("LLM_MAX_TOKENS")

    config = {
        "model": model,
        "api_key": TOGETHER_API_KEY,
        "temperature": float(temperature),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    return config


def embedding_config_from_env() -> Dict:
    model = os.getenv("EMBEDDING_MODEL")
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

    config = {
        "model_name": model,
        "api_key": TOGETHER_API_KEY,
    }
    return config


def init_settings():
    print("Running init_settings in the app.settings file ")
    llm_configs = llm_config_from_env()
    #embedding_configs = embedding_config_from_env()
    print(llm_configs)
    Settings.llm = TogetherLLM(**llm_configs)

    #Settings.embed_model = TogetherEmbedding(**embedding_configs)
    # Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
    # Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "20"))
