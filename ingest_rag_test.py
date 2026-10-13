
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.rag.services.ingestion_service import ingest_and_save_document

load_dotenv()

database_url = URL.create(
    "postgresql+psycopg",
    username=os.getenv("POSTGRES_USER", "postgres"),
    password=os.environ["POSTGRES_PASSWORD"],
    host="localhost",
    port=5433,
    database="fastapi_crud_db",
)

engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

try:
    records = ingest_and_save_document(
        db,
        "docs/project-documentation.pdf",
    )

    print(f"Chunks saved: {len(records)}")
    print(
        "Chunks with embeddings:",
        sum(record.embedding is not None for record in records),
    )

finally:
    db.close()
    engine.dispose()
