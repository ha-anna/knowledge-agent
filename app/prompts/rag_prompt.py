
from app.domain.search import SearchResult


def build_rag_messages(
    question: str,
    context: str,
) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": """
                You are a helpful knowledge assistant.

                Answer questions using only the provided context.

                Rules:
                - Use information from the context whenever possible.
                - Do not invent facts that are not supported by the context.
                - If the answer is not in the context, say you do not know.
                - Provide a clear and concise answer.
                - When listing information, include all relevant items from the context.
                - Preserve technical names, formulas, and terminology exactly.

                If the context contains insufficient information, explicitly say:
                    "I couldn't find this information in the uploaded documents."
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


def build_context(results):
    contexts = []

    for result in results:
        contexts.append(
            f"""
            Page {result.page_number}:
            {result.text}
            """
        )

    return "\n\n".join(contexts)

