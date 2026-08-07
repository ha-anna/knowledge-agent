from app.core.dependencies.rag import rag_service


def main():
    response = rag_service.answer(
        "What programming languages, frameworks, databases, and developer tools does Anna have experience with?"
    )

    print("=" * 50)
    print("ANSWER")
    print("=" * 50)
    print(response.answer)

    print()
    print("=" * 50)
    print("SOURCES")
    print("=" * 50)

    for source in response.sources:
        print("File:", source.filename)
        print("Page:", source.page_number)
        print("Distance:", source.distance)
        print("Snippet:", source.snippet)
        print()


if __name__ == "__main__":
    main()
