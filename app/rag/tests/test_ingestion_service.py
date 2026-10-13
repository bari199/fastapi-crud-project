
from app.rag.services.ingestion_service import ingest_document


def test_ingest_markdown_document(tmp_path):
    file_path = tmp_path / "README.md"
    file_path.write_text(
        "# FastAPI Project\n\nThis project uses PostgreSQL.",
        encoding="utf-8",
    )

    chunks = ingest_document(str(file_path))

    assert len(chunks) == 1
    assert chunks[0]["chunk_index"] == 0
    assert chunks[0]["source"] == "README.md"
    assert "PostgreSQL" in chunks[0]["text"]


def test_ingest_rejects_unsupported_file(tmp_path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("Some text", encoding="utf-8")

    try:
        ingest_document(str(file_path))
        assert False, "Expected ValueError"
    except ValueError:
        pass
