from app.core.dependencies.rag import rag_service


def main():
    response = rag_service.answer(
        "What technologies does Anna know?"
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
        print(source.filename)
        print(source.chunk_id)
        print()


if __name__ == "__main__":
    main()
