def build_rag_messages(
    question: str,
    context: str,
    history: list[dict[str, str]],
) -> list[dict[str, str]]:
    messages = [
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
                - Do not add information that is not explicitly stated.
                - Do not infer relationships or categories.
                - Do not classify items unless the context explicitly classifies them.
                - Preserve names exactly as written.
                - If the context contains a list, reproduce the list accurately.
                - If information is missing, say it is not specified.

                If the context contains insufficient information, explicitly say:
                    "I couldn't find this information in the uploaded documents."
                """,
        }
    ]

    for message in history:
        messages.append(
            {
                "role": message["role"],
                "content": message["content"],
            }
        )

    messages.append(
        {
            "role": "user",
            "content": (f"Context:\n{context}\n\nQuestion:\n{question}"),
        }
    )

    return messages


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
