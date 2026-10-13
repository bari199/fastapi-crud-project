
import json
from unittest.mock import MagicMock, patch

from app.rag.services.embedding_service import create_embeddings


def test_empty_input_returns_empty_list():
    assert create_embeddings([]) == []


def test_create_embeddings_returns_ollama_vectors():
    expected_vectors = [
        [0.1] * 768,
        [0.2] * 768,
    ]

    fake_response = MagicMock()
    fake_response.read.return_value = json.dumps({
        "embeddings": expected_vectors,
    }).encode("utf-8")

    with patch(
        "app.rag.services.embedding_service.urlopen",
        return_value=fake_response,
    ) as mock_urlopen:
        fake_response.__enter__ = MagicMock(
            return_value=fake_response
        )
        fake_response.__exit__ = MagicMock(return_value=False)

        vectors = create_embeddings(["first", "second"])

    assert vectors == expected_vectors

    request = mock_urlopen.call_args.args[0]
    assert request.full_url.endswith("/api/embed")

    payload = json.loads(request.data.decode("utf-8"))
    assert payload["model"] == "nomic-embed-text"
    assert payload["input"] == ["first", "second"]
