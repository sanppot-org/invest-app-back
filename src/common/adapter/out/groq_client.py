from groq import Groq

from src.config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY,
)


def chat(
    content: str,
    role: str = "user",
    model: str = "llama-3.3-70b-versatile",
) -> str | None:
    messages: list = [
        {
            "role": role,
            "content": content,
        },
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    return chat_completion.choices[0].message.content
