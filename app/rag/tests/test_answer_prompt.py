
from app.rag.prompts.answer_prompt import build_rag_prompt


def test_prompt_contains_question_and_context():
    prompt = build_rag_prompt(
        "Which database does this project use?",
        ["The project uses PostgreSQL."],
    )

    assert "Which database does this project use?" in prompt
    assert "The project uses PostgreSQL." in prompt


def test_prompt_instructs_model_not_to_invent():
    prompt = build_rag_prompt(
        "What is the deployment region?",
        ["The project uses FastAPI."],
    )

    assert "Do not invent facts." in prompt
    assert "does not provide enough information" in prompt


def test_prompt_handles_empty_context():
    prompt = build_rag_prompt("What is this project?", [])

    assert "What is this project?" in prompt
    assert "Context:" in prompt
