
from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)

from app.database import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    __table_args__ = (
        UniqueConstraint(
            "source",
            "chunk_index",
            name="uq_document_chunks_source_index",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String(500), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)

    # Ollama nomic-embed-text embeddings (768 dimensions)
    embedding = Column(Vector(768), nullable=True)
