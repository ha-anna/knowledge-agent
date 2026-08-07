from app.core.dependencies.vector_store import vector_store


def main():
    results = vector_store.search(
        query="What is this document about?",
        top_k=3,
    )

    print(f"Found {len(results)} results")

    for result in results:
        print("=" * 50)
        print("Filename:", result.filename)
        print("Document ID:", result.document_id)
        print("Chunk ID:", result.chunk_id)
        print("Distance:", result.distance)
        print()
        print(result.text[:500])


if __name__ == "__main__":
    main()
