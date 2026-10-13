
import json
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def create_embeddings(texts: list[str]) -> list[list[float]]:
    """Create local embeddings using Ollama."""

    if not texts:
        return []

    base_url = os.getenv(
        "OLLAMA_BASE_URL",
        "http://host.docker.internal:11434",
    ).rstrip("/")
    model = os.getenv(
        "OLLAMA_EMBED_MODEL",
        "nomic-embed-text",
    )

    payload = json.dumps({
        "model": model,
        "input": texts,
    }).encode("utf-8")

    request = Request(
        f"{base_url}/api/embed",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (URLError, HTTPError, TimeoutError) as exc:
        raise RuntimeError(
            f"Could not generate embeddings using Ollama: {exc}"
        ) from exc

    embeddings = result.get("embeddings", [])

    if len(embeddings) != len(texts):
        raise RuntimeError(
            "Ollama returned an unexpected number of embeddings."
        )

    for embedding in embeddings:
        if len(embedding) != 768:
            raise RuntimeError(
                f"Expected 768 embedding dimensions, got {len(embedding)}."
            )

    return embeddings
