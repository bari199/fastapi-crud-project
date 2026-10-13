
from pathlib import Path

from sqlalchemy.orm import Session

from app.rag.chunking.text_chunker import chunk_text
from app.rag.document_loaders.markdown_loader import load_markdown
from app.rag.document_loaders.pdf_loader import load_pdf
from app.rag.services.document_repository import save_chunks
from app.rag.services.embedding_service import create_embeddings
from app.rag.services.vector_store import store_embeddings


def ingest_document(file_path: str) -> list[dict]:
    """Load a PDF or Markdown document and split it into chunks."""

    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        text = load_pdf(str(path))
    elif suffix in {".md", ".markdown"}:
        text = load_markdown(str(path))
    else:
        raise ValueError("Supported file types: PDF, .md, .markdown")

    chunks = chunk_text(text)

    return [
        {
            "chunk_index": index,
            "text": chunk,
            "source": path.name,
        }
        for index, chunk in enumerate(chunks)
    ]


def ingest_and_save_document(
    db: Session,
    file_path: str,
) -> list:
    """Load, chunk, embed, and save a document."""

    chunks = ingest_document(file_path)

    if not chunks:
        return []

    # 1. Generate embeddings locally using Ollama.
    embeddings = create_embeddings(
        [chunk["text"] for chunk in chunks]
    )

    # 2. Save chunks to PostgreSQL.
    records = save_chunks(db, chunks)

    # 3. Attach the generated vectors to those records.
    return store_embeddings(db, records, embeddings)
