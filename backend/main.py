from dotenv import load_dotenv

load_dotenv()

import logging
import os
import uvicorn

from typing import List
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.api.routers.chat import chat_router
from app.settings import init_settings
from app.vectara.vectara_index import index_file
from app.api.routers.file import file_router

app = FastAPI()

# calling init setting for initial set up (creating embeddings and llm)
init_settings()

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set

# Conditions setup for development environment
if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Redirect to documentation page when accessing base URL
    @app.get("/")
    async def redirect_to_docs():
        return RedirectResponse(url="/docs")

# Including routers
app.include_router(file_router)
app.include_router(chat_router, prefix="/api/chat")

# Main execution block
if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "8000"))
    reload = True if environment == "dev" else False

    uvicorn.run(app="main:app", host=app_host, port=app_port, reload=reload)
