import os
from collections import defaultdict

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider

load_dotenv(".env")


class AppState:
    agent: Agent
    histories: defaultdict[int, list[ModelMessage]] = defaultdict(list)

    @classmethod
    def set_agent(cls):
        api_key = os.getenv("GROQ_API_KEY")

        model = GroqModel(
            "llama-3.3-70b-versatile",
            provider=GroqProvider(api_key=api_key),
        )

        cls.agent = Agent(model, instructions="日本語で解答してください。")


AppState.set_agent()
