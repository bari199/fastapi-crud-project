
import pytest
from unittest.mock import MagicMock, patch

from app.rag.retrieval.retriever import retrieve_relevant_chunks


def test_retrieve_rejects_wrong_embedding_dimensions():
    db = MagicMock()

    with pytest.raises(ValueError, match="768 dimensions"):
        retrieve_relevant_chunks(db, [0.1, 0.2])

    db.scalars.assert_not_called()


def test_retrieve_rejects_invalid_limit():
    db = MagicMock()

    with pytest.raises(ValueError, match="greater than 0"):
        retrieve_relevant_chunks(db, [0.1] * 768, limit=0)

    db.scalars.assert_not_called()


def test_retrieve_returns_database_results():
    db = MagicMock()
    expected_chunks = [MagicMock(), MagicMock()]

    result = MagicMock()
    result.all.return_value = expected_chunks
    db.scalars.return_value = result

    with patch(
        "app.rag.retrieval.retriever.select"
    ) as mock_select:
        mock_select.return_value.where.return_value.order_by.return_value.limit.return_value = (
            MagicMock()
        )

        chunks = retrieve_relevant_chunks(db, [0.1] * 768)

    assert chunks == expected_chunks
    db.scalars.assert_called_once()
