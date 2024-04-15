import os
from app.engine.index import get_index
from llama_index.core.settings import Settings
# from llama_index.core.chat_engine.types import (
#     BaseChatEngine, SimpleChatEngine
# )
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core import ServiceContext
from llama_index.llms.together import TogetherLLM


# def get_chat_engine():
#     system_prompt = os.getenv("SYSTEM_PROMPT")
#     top_k = os.getenv("TOP_K", 3)

#     # Calling get index function
#     print("Calling get index function")
#     index = get_index()

#     print("done getting index function on get_chat_engine")
#     if index is None:
#         raise Exception(
#             "StorageContext is empty - call 'python app/engine/generate.py' to generate the storage first"
#         )

#     return index.as_chat_engine(
#         similarity_top_k=int(top_k),
#         system_prompt=system_prompt,
#         chat_mode="condense_plus_context",
#     )


def get_chat_engine():
    # Create a service context with the desired LLM
    print(Settings.llm)
    service_context = ServiceContext.from_defaults(
        llm=Settings.llm,
        embed_model = Settings.embed_model
    )

    # Create and return a SimpleChatEngine instance
    chat_engine = SimpleChatEngine.from_defaults(service_context=service_context)
    return chat_engine

