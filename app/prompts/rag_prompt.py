
from app.domain.search import SearchResult


def build_rag_prompt(question: str, context: str) -> str:
    return PROMPT_TEMPLATE.format(
        context=context,
        question=question,
    )


PROMPT_TEMPLATE = """
You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say that you don't know.

Context:
{context}

Question:
{question}

Answer:
""".strip()


def build_context(
    results: list[SearchResult],
) -> str:
    parts = []

    for result in results:
        parts.append(
            f"""
                Document: {result.filename}

                Content:
                {result.text}
                """
                    )

    return "\n\n----------------\n\n".join(parts)
