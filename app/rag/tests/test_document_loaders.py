
from pathlib import Path

from app.rag.document_loaders.markdown_loader import load_markdown
from app.rag.document_loaders.pdf_loader import load_pdf


def test_markdown_loader(tmp_path: Path):
    file_path = tmp_path / "README.md"
    file_path.write_text("# RAG Test\n\nHello FastAPI!", encoding="utf-8")

    text = load_markdown(str(file_path))

    assert "# RAG Test" in text
    assert "Hello FastAPI!" in text


def test_markdown_loader_rejects_wrong_extension(tmp_path: Path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("Some text", encoding="utf-8")

    try:
        load_markdown(str(file_path))
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_pdf_loader_rejects_wrong_extension(tmp_path: Path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("Some text", encoding="utf-8")

    try:
        load_pdf(str(file_path))
        assert False, "Expected ValueError"
    except ValueError:
        pass
