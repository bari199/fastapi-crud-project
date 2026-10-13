
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.rag.models import DocumentChunk


def retrieve_relevant_chunks(
    db: Session,
    query_embedding: list[float],
    limit: int = 5,
) -> list[DocumentChunk]:
    """Retrieve the most relevant chunks using cosine distance."""

    if len(query_embedding) != 768:
        raise ValueError(
            "Query embedding must contain 768 dimensions."
        )

    if limit <= 0:
        raise ValueError("limit must be greater than 0.")

    statement = (
        select(DocumentChunk)
        .where(DocumentChunk.embedding.is_not(None))
        .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )

    return list(db.scalars(statement).all())
