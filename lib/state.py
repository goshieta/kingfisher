import os
from collections import defaultdict

from dotenv import load_dotenv
from pydantic_ai import Agent, WebSearchTool
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

load_dotenv(".env")


class AppState:
    agent: Agent
    histories: defaultdict[int, list[ModelMessage]] = defaultdict(list)

    @classmethod
    def set_agent(cls):
        api_key = os.getenv("GOOGLE_API_KEY")

        model = GoogleModel(
            "gemini-2.5-flash", provider=GoogleProvider(api_key=api_key)
        )

        cls.agent = Agent(
            model,
            instructions="日本語で解答してください。",
            builtin_tools=[WebSearchTool()],
        )


AppState.set_agent()
