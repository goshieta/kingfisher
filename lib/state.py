import os
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

load_dotenv(".env")


class AppState:
    agent: Agent
    histories: defaultdict[int, list[ModelMessage]] = defaultdict(list)
    NOTES_DIR: Path = Path("memory")

    @classmethod
    def set_agent(cls):
        api_key = os.getenv("GOOGLE_API_KEY")

        model = GoogleModel(
            "gemini-2.5-flash-lite", provider=GoogleProvider(api_key=api_key)
        )

        from lib.build_instructions import build_instructions

        cls.agent = Agent(
            model,
            instructions=build_instructions,
            builtin_tools=[],
        )

        import lib.tools.fetch  # noqa: F401
        import lib.tools.rwfile  # noqa: F401
        import lib.tools.search  # noqa: F401

    @classmethod
    def init_notes_dir(cls):
        cls.NOTES_DIR.mkdir(exist_ok=True)
