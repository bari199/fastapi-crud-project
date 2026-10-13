
import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.rag.models import DocumentChunk
from app.rag.services.ingestion_service import ingest_and_save_document


@pytest.fixture
def test_db():
    database_url = os.getenv("RAG_TEST_DATABASE_URL")

    if not database_url:
        pytest.skip("RAG_TEST_DATABASE_URL is not configured")

    engine = create_engine(database_url)

    try:
        Base.metadata.create_all(bind=engine)
        TestingSession = sessionmaker(bind=engine)

        with TestingSession() as db:
            yield db

    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_markdown_ingestion_saves_chunks(test_db, tmp_path: Path):
    file_path = tmp_path / "README.md"
    file_path.write_text(
        "# FastAPI RAG\n\nThis project uses PostgreSQL and pgvector.",
        encoding="utf-8",
    )

    saved_chunks = ingest_and_save_document(test_db, str(file_path))

    assert len(saved_chunks) == 1
    assert saved_chunks[0].source == "README.md"
    assert "PostgreSQL" in saved_chunks[0].text

    result = test_db.scalars(
        select(DocumentChunk).where(
            DocumentChunk.source == "README.md"
        )
    ).all()

    assert len(result) == 1
    assert result[0].chunk_index == 0
