from typing import List, Literal

from pydantic import Field, BaseModel

Operator = Literal["<->", "<=>", "<#>"]
MergeStrategy = Literal["score_normalization", "rrf"]

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
    merge_strategy: MergeStrategy = Field(default="score_normalization")

class DocumentResult(BaseModel):
    id: int = Field()
    title: str = Field()
    content: str = Field()
    semantic_score: float = Field(default=0.0)
    bm25_score: float = Field(default=0.0)
    hybrid_score: float = Field(default=0.0)

    def __eq__(self, other):
        return isinstance(other, DocumentResult) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

class QueryResult(BaseModel):
    documents: List[DocumentResult]
