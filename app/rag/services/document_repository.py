
from sqlalchemy.orm import Session

from app.rag.models import DocumentChunk


def save_chunks(
    db: Session,
    chunks: list[dict],
) -> list[DocumentChunk]:
    """Save chunks while skipping existing source/index pairs."""

    records = []
    seen_keys = set()

    try:
        for chunk in chunks:
            source = chunk["source"]
            chunk_index = chunk["chunk_index"]
            key = (source, chunk_index)

            if key in seen_keys:
                continue

            seen_keys.add(key)

            existing = (
                db.query(DocumentChunk)
                .filter(
                    DocumentChunk.source == source,
                    DocumentChunk.chunk_index == chunk_index,
                )
                .first()
            )

            if existing is not None:
                continue

            records.append(
                DocumentChunk(
                    source=source,
                    chunk_index=chunk_index,
                    text=chunk["text"],
                    metadata_json=chunk.get("metadata_json"),
                    embedding=None,
                )
            )

        if not records:
            return []

        db.add_all(records)
        db.commit()

        for record in records:
            db.refresh(record)

        return records

    except Exception:
        db.rollback()
        raise
