
from pathlib import Path


def load_markdown(file_path: str) -> str:
    """Read text from a Markdown or README file."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Markdown file not found: {path}")

    if path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("Expected a .md or .markdown file.")

    return path.read_text(encoding="utf-8").strip()
