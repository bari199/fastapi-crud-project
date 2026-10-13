
from sqlalchemy.orm import Session

from app.rag.models import DocumentChunk


def store_embeddings(
    db: Session,
    records: list[DocumentChunk],
    embeddings: list[list[float]],
) -> list[DocumentChunk]:
    """Attach embedding vectors to saved document chunks."""

    if len(records) != len(embeddings):
        raise ValueError(
            "The number of records and embeddings must match."
        )

    for record, embedding in zip(records, embeddings):
        if len(embedding) != 768:
            raise ValueError(
                "Each embedding must contain 768 dimensions."
            )

        record.embedding = embedding

    try:
        db.commit()

        for record in records:
            db.refresh(record)

        return records

    except Exception:
        db.rollback()
        raise
