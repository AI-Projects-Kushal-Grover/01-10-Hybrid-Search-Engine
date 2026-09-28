from typing import Annotated

from fastapi import APIRouter, Query

from app.domain.models import QueryRequest
from app.services.semantic_search import SemanticSearch

router = APIRouter()

semantic_search = SemanticSearch()

@router.get("/query")
async def query(query: Annotated[QueryRequest, Query()]):
    return await semantic_search.search(query.search, query.operator, query.normalize_embeddings)
