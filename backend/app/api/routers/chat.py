from pydantic import BaseModel
from typing import List, Any, Optional, Dict, Tuple
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from llama_index.core.chat_engine.types import (
    BaseChatEngine,
)
from llama_index.core.settings import Settings

from llama_index.core.schema import NodeWithScore
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.litellm import LiteLLM

from app.engine import get_chat_engine
from app.vectara.vectara_index import create_vectara_response
#from app.vectara.vectara_index import filter_response

chat_router = r = APIRouter()


class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "What standards for letters exist?",
                    }
                ]
            }
        }


class _SourceNodes(BaseModel):
    id: str
    metadata: Dict[str, Any]
    score: Optional[float]

    @classmethod
    def from_source_node(cls, source_node: NodeWithScore):
        return cls(
            id=source_node.node.node_id,
            metadata=source_node.node.metadata,
            score=source_node.score,
        )

    @classmethod
    def from_source_nodes(cls, source_nodes: List[NodeWithScore]):
        return [cls.from_source_node(node) for node in source_nodes]


class _Result(BaseModel):
    result: _Message
    nodes: List[_SourceNodes]


async def parse_chat_data(data: _ChatData) -> Tuple[str, List[ChatMessage]]:
    # check preconditions and get last message
    print("Calling parse_chat_data from routers.chat.py")
    print(data)
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    last_message = data.messages.pop()
    if last_message.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )
    # convert messages coming from the request to type ChatMessage
    messages = [
        ChatMessage(
            role=m.role,
            content=m.content,
        )
        for m in data.messages
    ]
    print("This is the message from the user")
    print(last_message.content, messages)
    return last_message.content, messages


# streaming endpoint - delete if not needed
@r.post("")
async def chat(
    request: Request,
    data: _ChatData,
):
    #last message content is the input in string, messages is the message history
    last_message_content, messages = await parse_chat_data(data)

    # response = await chat_engine.astream_chat(last_message_content, messages)
    # print("Executing streaming end point, chat")
    # print(Settings.llm)
    # response = await chat_engine.astream_chat(last_message_content, messages)
    vectara_response = create_vectara_response(last_message_content)

    #filtered_response = filter_response(vectara_response)  # Assume this function is defined to filter the response

    print("done running response")
    # async def event_generator():
    #     yield filtered_response  
    # return StreamingResponse(event_generator(), media_type="text/plain")
    return vectara_response

# @r.post("")
# async def chat(
#     request: Request,
#     data: _ChatData,
#     #chat_engine: BaseChatEngine = Depends(get_chat_engine),
# ):
#     last_message_content, messages = await parse_chat_data(data)
#     # print("Executing streaming end point, chat")
#     response = await chat_engine.astream_chat(last_message_content, messages)

#     print("done running respose")
#     async def event_generator():
#         async for token in response.async_response_gen():
#             if await request.is_disconnected():
#                 break
#             yield token

#     return StreamingResponse(event_generator(), media_type="text/plain")

