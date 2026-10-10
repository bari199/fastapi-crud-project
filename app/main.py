
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app import models
from app.database import Base, engine
from app.routes.tasks import router as tasks_router
from app.routes.auth import router as auth_router

app = FastAPI(
    title="FastAPI Task Management API",
    description="CRUD API using FastAPI and PostgreSQL",
    version="1.0.0",
)

# Create tables for this learning project
Base.metadata.create_all(bind=engine)

# Register task endpoints
app.include_router(tasks_router)
app.include_router(auth_router)

@app.get("/", tags=["General"])
def root():
    return {"message": "Welcome to the Task Management API"}


@app.get("/health/db", tags=["General"])
def check_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "success",
            "database": "PostgreSQL connected",
        }

    except SQLAlchemyError:
        return {
            "status": "error",
            "database": "Connection failed",
        }
