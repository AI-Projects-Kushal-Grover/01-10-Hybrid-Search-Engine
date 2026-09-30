from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables from .env file
env_file = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_file)

from app.api.documents import router as document_router
from app.api.query import router as query_router
from app.services import keyword_search
from app.repositories import document_chunk_repository

@asynccontextmanager
async def lifespan(app: FastAPI):
    await document_chunk_repository.create_table_if_not_exists()
    await keyword_search.index_keywords()
    yield

app = FastAPI(
    title="Semantic Search Engine",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(document_router)
app.include_router(query_router)
