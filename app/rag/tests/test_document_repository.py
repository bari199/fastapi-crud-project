
from unittest.mock import MagicMock

import pytest

from app.rag.services.document_repository import save_chunks


def test_save_chunks_commits_records():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    chunks = [
        {
            "source": "README.md",
            "chunk_index": 0,
            "text": "This project uses FastAPI.",
        },
        {
            "source": "README.md",
            "chunk_index": 1,
            "text": "This project uses PostgreSQL.",
        },
    ]

    records = save_chunks(db, chunks)

    assert len(records) == 2
    assert records[0].source == "README.md"
    assert records[0].chunk_index == 0
    assert records[0].text == "This project uses FastAPI."
    assert records[0].embedding is None

    db.add_all.assert_called_once_with(records)
    db.commit.assert_called_once()
    assert db.refresh.call_count == 2


def test_save_chunks_skips_existing_records():
    db = MagicMock()
    existing_record = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = (
        existing_record
    )

    chunks = [
        {
            "source": "README.md",
            "chunk_index": 0,
            "text": "This project uses FastAPI.",
        }
    ]

    records = save_chunks(db, chunks)

    assert records == []
    db.add_all.assert_not_called()
    db.commit.assert_not_called()


def test_save_chunks_skips_duplicate_input_chunks():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    chunk = {
        "source": "README.md",
        "chunk_index": 0,
        "text": "This project uses FastAPI.",
    }

    records = save_chunks(db, [chunk, chunk])

    assert len(records) == 1
    db.add_all.assert_called_once_with(records)
    db.commit.assert_called_once()


def test_save_chunks_rolls_back_on_error():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    db.commit.side_effect = RuntimeError("Database error")

    chunks = [
        {
            "source": "README.md",
            "chunk_index": 0,
            "text": "Test content",
        }
    ]

    with pytest.raises(RuntimeError, match="Database error"):
        save_chunks(db, chunks)

    db.rollback.assert_called_once()
