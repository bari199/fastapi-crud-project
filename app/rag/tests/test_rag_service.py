
import pytest
from unittest.mock import MagicMock, patch

from app.rag.services.rag_service import answer_question


def test_empty_question_is_rejected():
    with pytest.raises(ValueError, match="Question cannot be empty"):
        answer_question(MagicMock(), "   ")


def test_invalid_top_k_is_rejected():
    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        answer_question(MagicMock(), "What is this project?", top_k=0)


def test_no_relevant_chunks_returns_fallback():
    db = MagicMock()

    with patch(
        "app.rag.services.rag_service.create_embeddings",
        return_value=[[0.1] * 768],
    ), patch(
        "app.rag.services.rag_service.retrieve_relevant_chunks",
        return_value=[],
    ):
        result = answer_question(db, "What is this project?")

    assert result["sources"] == []
    assert "could not find relevant information" in result["answer"]
