# システムプロンプトを作成する
import asyncio
from datetime import datetime
from pathlib import Path

from pydantic_ai import RunContext

from lib.manage_daily import handover_daily
from lib.state import AppState

INSTRUCTIONS_TEMPLATE = Path("prompt/instructions.md").read_text(encoding="utf-8")
NOTES_DIR = AppState.NOTES_DIR


def build_instructions(ctx: RunContext) -> str:
    ai_characteristics = (NOTES_DIR / "AGENT.md").read_text(encoding="utf-8")
    user_characteristics = (NOTES_DIR / "USER.md").read_text(encoding="utf-8")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    daily_path = NOTES_DIR / f"Daily/{datetime.today().strftime('%Y-%m-%d')}.md"
    if daily_path.exists():
        daily = daily_path.read_text(encoding="utf-8")
    else:
        daily = Path("prompt/daily.md").read_text(encoding="utf-8")
        asyncio.run(handover_daily())

    return INSTRUCTIONS_TEMPLATE.format(
        ai_characteristics=ai_characteristics,
        user_characteristics=user_characteristics,
        daily=daily,
        date=date,
    )
