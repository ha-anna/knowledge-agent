
from app.domain.search import SearchResult


def build_rag_messages(
    question: str,
    context: str,
) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": """
                You are a document question answering assistant.

                Rules:
                1. Answer only using the provided context.
                2. Do not classify, categorize, or reorganize information unless the user asks.
                3. Do not infer missing information.
                4. If something is not explicitly stated, say it is not specified.
                5. Keep answers concise.
                6. Do not mention "the provided context".
                7. Cite page numbers when possible.
                """,
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Question:\n{question}"
            ),
        },
    ]


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
