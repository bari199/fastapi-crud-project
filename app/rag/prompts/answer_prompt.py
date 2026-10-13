
def build_rag_prompt(question: str, contexts: list[str]) -> str:
    """Build a grounded prompt from retrieved document chunks."""

    context_text = "\n\n---\n\n".join(contexts)

    return f"""
You are a helpful assistant answering questions about project documentation.

Answer the question using only the context provided below.
If the context does not contain the answer, say that the available
documentation does not provide enough information.
Do not invent facts.

Context:
{context_text}

Question:
{question}

Answer:
""".strip()
