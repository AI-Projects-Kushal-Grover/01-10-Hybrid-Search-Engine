from typing import Annotated

from fastapi import APIRouter, Query

from app.domain.models import QueryRequest
from app.handlers.query_handler import QueryHandler

router = APIRouter()

query_handler = QueryHandler()

@router.get("/query")
async def query(query: Annotated[QueryRequest, Query()]):
    return await query_handler.search(query)
