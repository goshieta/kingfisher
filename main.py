import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider

load_dotenv(".env")
api_key = os.getenv("GROQ_API_KEY")

model = GroqModel(
    "llama-3.3-70b-versatile",
    provider=GroqProvider(api_key=api_key),
)

agent = Agent(model, instructions="日本語で解答してください。")


def main():
    mes = input("メッセージを入力: ")
    result = agent.run_sync(mes)
    print(result.output)


if __name__ == "__main__":
    main()
