import os
import logging
from typing import List, cast, LiteralString

from psycopg import sql

from app.domain.models import Operator
from app.infrastructure.database import Database
from app.domain.entities import DocumentChunk

logger = logging.getLogger(__name__)

database = Database(os.getenv("PG_CONNECTION_STRING", ""))

class DocumentChunkRepository():
    def __init__(self) -> None:
        self.table_name = "document_chunk"
        pass

    async def create_table_if_not_exists(self):
        query = self._compose_query("""
            CREATE TABLE IF NOT EXISTS {} (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                title varchar(200),
                content text,
                embedding vector(384)
            )
        """)
        try:
            logger.info("Creating table if not exists: %s", self.table_name)
            result = await database.execute(query)
            logger.info("Table ensured: %s", self.table_name)
            return result
        except Exception as ee:
            logger.exception("Failed to create or ensure table %s", self.table_name)
            raise

    async def insert(self, vector_store: DocumentChunk):
        query = self._compose_query("INSERT INTO {} (title, content, embedding) values (%s, %s, %s)")
        await database.execute(
            query,
            (vector_store.title, vector_store.content, vector_store.embedding)
        )

    async def select_by_embeddings(self, embedding: List[float], operator: Operator, limit = 5):
        query = sql.SQL("SELECT id, title, content, (embedding {op} %s::vector) as distance FROM {table} ORDER BY distance LIMIT %s").format(
            table=sql.Identifier(self.table_name),
            op=sql.SQL(cast(LiteralString, operator))
        )
        results = await database.execute(
            query,
            (embedding, limit)
        )
        return await results.fetchall()

    async def select_all(self):
        query = sql.SQL("SELECT id, title, content FROM {table}").format(
            table=sql.Identifier(self.table_name),
        )
        results = await database.execute(query)
        return await results.fetchall()

    def _compose_query(self, query) -> sql.Composed:
        return sql.SQL(query).format(sql.Identifier(self.table_name))