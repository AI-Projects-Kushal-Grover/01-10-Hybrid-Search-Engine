from typing import List, Literal

from pydantic import Field, BaseModel

class Document(BaseModel):
    title: str = Field(max_length=200)
    content: str = Field()
    chunk_size: int = Field(default=400)
    chunk_overlap: int = Field(default=50)
    normalize_embeddings: bool = Field(default=True)

class QueryRequest(BaseModel):
    search: str = Field()
    operator: Literal["<->", "<=>", "<#>"]
    normalize_embeddings: bool = Field(default=True)

class DocumentResult(BaseModel):
    title: str = Field()
    content: str = Field()
    distance: float = Field()

class QueryResult(BaseModel):
    documents: List[DocumentResult]
