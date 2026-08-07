from ollama import Client

from app.core.config import settings


def main():
    client = Client(
        host=settings.ollama_base_url,
    )

    response = client.chat(
        model=settings.ollama_model,
        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence, make a joke.",
            }
        ],
    )

    print(response["message"]["content"])


if __name__ == "__main__":
    main()
