from pathlib import Path
from pypdf import PdfReader


def load_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Expected a PDF file.")

    reader = PdfReader(str(path))
    pages = []

    for page in reader.pages:
        pages.append(page.extract_text() or "")

    return "\n\n".join(pages).strip()