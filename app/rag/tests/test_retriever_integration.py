
import os
from urllib.parse import urlparse

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.rag.models import DocumentChunk
from app.rag.retrieval.retriever import retrieve_relevant_chunks


@pytest.fixture
def test_db():
    database_url = os.getenv("RAG_TEST_DATABASE_URL")

    if not database_url:
        pytest.skip("RAG_TEST_DATABASE_URL is not configured")

    database_name = urlparse(database_url).path.lstrip("/")

    # Never run destructive test setup against the main database.
    if database_name != "fastapi_rag_test_db":
        pytest.fail("This integration test requires fastapi_rag_test_db")

    engine = create_engine(database_url)

    try:
        Base.metadata.create_all(bind=engine)
        TestingSession = sessionmaker(bind=engine)

        with TestingSession() as db:
            yield db

    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_retrieves_nearest_vector_first(test_db):
    query_vector = [1.0, 0.0] + [0.0] * 766
    relevant_vector = [0.99, 0.01] + [0.0] * 766
    unrelated_vector = [0.0, 1.0] + [0.0] * 766

    relevant = DocumentChunk(
        source="README.md",
        chunk_index=0,
        text="This project uses FastAPI and PostgreSQL.",
        embedding=relevant_vector,
    )

    unrelated = DocumentChunk(
        source="notes.md",
        chunk_index=0,
        text="This document discusses unrelated topics.",
        embedding=unrelated_vector,
    )

    no_embedding = DocumentChunk(
        source="draft.md",
        chunk_index=0,
        text="This chunk has no embedding yet.",
        embedding=None,
    )

    test_db.add_all([relevant, unrelated, no_embedding])
    test_db.commit()

    results = retrieve_relevant_chunks(
        test_db,
        query_vector,
        limit=2,
    )

    assert len(results) == 2
    assert results[0].text == "This project uses FastAPI and PostgreSQL."
    assert all(item.embedding is not None for item in results)
