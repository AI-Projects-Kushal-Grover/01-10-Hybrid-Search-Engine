from typing import List, Literal

from pydantic import Field, BaseModel

Operator = Literal["<->", "<=>", "<#>"]
MergeStrategy = Literal["candidiate_merging", "score_normalization", "rrf"]

class Document(BaseModel):
    title: str = Field(max_length=200)
    content: str = Field()
    chunk_size: int = Field(default=400)
    chunk_overlap: int = Field(default=50)
    normalize_embeddings: bool = Field(default=True)

class QueryRequest(BaseModel):
    search: str = Field()
    operator: Operator = Field(default="<->")
    normalize_embeddings: bool = Field(default=True)
    merge_strategy: MergeStrategy = Field(default="candidiate_merging")

class DocumentResult(BaseModel):
    id: int = Field()
    title: str = Field()
    content: str = Field()
    distance: float | None = Field(default=None)

class QueryResult(BaseModel):
    documents: List[DocumentResult]
