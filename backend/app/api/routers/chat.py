from pydantic import BaseModel
from typing import List, Any, Optional, Dict, Tuple
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from llama_index.core.chat_engine.types import (
    BaseChatEngine,
)
from llama_index.core.settings import Settings
from fastapi.responses import JSONResponse

from llama_index.core.schema import NodeWithScore
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.litellm import LiteLLM

from app.engine import get_chat_engine
from app.vectara.vectara_index import create_vectara_response
import asyncio
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

@r.post("")
async def chat(request: Request, data: _ChatData):
    last_message_content, messages = await parse_chat_data(data)

    async def event_generator(query):
        try:
            response = create_vectara_response(query)
            if isinstance(response, str):
                # Split response into lines for streaming if it's a single string
                for line in response.splitlines(keepends=True):  # keepends=True to keep newlines
                    yield line
                    await asyncio.sleep(0.1)  # Simulate delay for streaming effect
            elif hasattr(response, '__iter__'):
                # If response is an iterable, iterate and stream each item
                for item in response:
                    if isinstance(item, str):
                        yield item + '\n'
                    else:
                        yield f"{item}\n"  # Convert item to string if not already
                    await asyncio.sleep(0.1)
            else:
                # Directly yield the response if it is not string or iterable
                yield str(response) + '\n'
        except Exception as e:
            yield f"Error generating response: {str(e)}\n"  # Provide error message

    return StreamingResponse(event_generator(last_message_content), media_type="text/event-stream")

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

