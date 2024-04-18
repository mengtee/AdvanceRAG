from pydantic import BaseModel
from typing import List, Any, Optional, Dict, Tuple
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from llama_index.core.chat_engine.types import (
    BaseChatEngine,
)
import os
from app.vectara.vectara_index import index_file
import logging


import asyncio

# Setup router for file operations
file_router = APIRouter()

# Getting the directory of available files
@file_router.get("/files/", response_model=List[str])
async def list_files() -> List[str]:
    files_dir = "/Users/Development/AdvanceRAG/vectara-implementation/backend/data"
    try:
        files = os.listdir(files_dir)
        return [file for file in files if os.path.isfile(os.path.join(files_dir, file))]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class FileRequest(BaseModel):
    file_name: str

@file_router.post("/process-file/")
async def process_file(file_request: FileRequest):
    file_name = file_request.file_name
    files_dir = "/Users/Development/AdvanceRAG/vectara-implementation/backend/data"
    file_path = os.path.join(files_dir, file_name)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    print(f"Processing file: {file_name}")

    logger = logging.getLogger("uvicorn")
    logger.info(f"Processing file: {file_name}, calling from file api")

    # Assume `vectara_index` is a module you've written that can index files
    index_success = index_file(file_path)  # Example function call to index the file

    if not index_success:
        raise HTTPException(status_code=500, detail="Failed to index file")
    
    return {"message": f"File {file_name} processed successfully", "file_name": file_name}
