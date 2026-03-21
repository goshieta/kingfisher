from datetime import datetime
from pathlib import Path

from lib.state import AppState


async def handover_daily():
    date_str = datetime.now().strftime("%Y-%m-%d")

    daily_dir_path = AppState.NOTES_DIR / "Daily"
    daily_dir_path.mkdir(exist_ok=True)
    daily_path = daily_dir_path / f"{date_str}.md"
    daily_template_path = Path("prompt/daily.md")

    late_str = max(
        (f.stem for f in daily_dir_path.glob("*-*-*.md")),
        key=lambda x: datetime.strptime(x, "%Y-%m-%d"),
        default=None,
    )

    template_content = daily_template_path.read_text(encoding="utf-8")
    daily_path.write_text(
        template_content.replace(f"{date_str}", date_str), encoding="utf-8"
    )

    if late_str:
        handover = Path("prompt/handover_daily.md").read_text(encoding="utf-8")
        await AppState.agent.run(handover.format(today=date_str, late=late_str))
