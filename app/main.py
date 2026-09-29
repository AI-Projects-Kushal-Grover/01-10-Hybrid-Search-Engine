from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables from .env file
env_file = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_file)

from app.infrastructure.database import Database
from app.api.documents import router as document_router
from app.api.query import router as query_router
from app.repositories.document_chunk import DocumentChunkRepository
from app.services.keyword_search import KeywordSearch

@asynccontextmanager
async def lifespan(app: FastAPI):
    document_chunk_repo = DocumentChunkRepository()
    await document_chunk_repo.create_table_if_not_exists()

    keyword_search = KeywordSearch()
    await keyword_search.index_keywords()
    yield

app = FastAPI(
    title="Semantic Search Engine",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(document_router)
app.include_router(query_router)
