
from app.domain.search import SearchResult


def build_rag_messages(
    question: str,
    context: str,
) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": """
                You answer questions using only the provided context.

                Rules:
                - Extract only explicitly mentioned technical skills.
                - Ignore spoken languages and communication skills.
                - Ignore job titles, soft skills, certifications, and tools unless they are software/technical tools.
                - Do not infer related technologies.
                - Do not include explanations.
                - Return only a comma-separated list of technologies.

                Example:
                HTML, CSS, JavaScript, React, Node.js

                If no technologies are found, return:
                None
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

