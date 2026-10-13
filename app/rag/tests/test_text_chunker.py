
from app.rag.chunking.text_chunker import chunk_text


def test_empty_text_returns_empty_list():
    assert chunk_text("") == []


def test_short_text_returns_one_chunk():
    assert chunk_text("Hello FastAPI") == ["Hello FastAPI"]


def test_long_text_is_split_with_overlap():
    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        chunk_overlap=150,
    )

    assert len(chunks) == 3
    assert len(chunks[0]) == 1000
    assert len(chunks[1]) == 1000
    assert len(chunks[2]) == 800


def test_invalid_chunk_size_raises_error():
    try:
        chunk_text("Hello", chunk_size=0)
        assert False, "Expected ValueError"
    except ValueError:
        pass
