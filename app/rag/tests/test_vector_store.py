
from unittest.mock import MagicMock

import pytest

from app.rag.services.vector_store import store_embeddings


def test_store_embeddings_assigns_vectors():
    db = MagicMock()

    record = MagicMock()
    records = [record]

    vector = [0.1] * 768

    result = store_embeddings(db, records, [vector])

    assert result == records
    assert record.embedding == vector
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(record)


def test_store_embeddings_rejects_wrong_dimensions():
    db = MagicMock()
    record = MagicMock()

    with pytest.raises(ValueError, match="768 dimensions"):
        store_embeddings(db, [record], [[0.1, 0.2]])

    db.commit.assert_not_called()


def test_store_embeddings_rejects_mismatched_counts():
    db = MagicMock()

    with pytest.raises(ValueError, match="must match"):
        store_embeddings(db, [MagicMock()], [])

    db.commit.assert_not_called()


def test_store_embeddings_rolls_back_on_commit_error():
    db = MagicMock()
    db.commit.side_effect = RuntimeError("Database error")

    record = MagicMock()

    with pytest.raises(RuntimeError, match="Database error"):
        store_embeddings(db, [record], [[0.1] * 768])

    db.rollback.assert_called_once()
