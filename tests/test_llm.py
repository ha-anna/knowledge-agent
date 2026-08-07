from app.core.dependencies.llm import llm_service


def main():
    answer = llm_service.generate(
        "What is recursion? Answer in one sentence."
    )

    print(answer)


if __name__ == "__main__":
    main()
