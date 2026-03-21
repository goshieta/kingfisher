import os
import shutil
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

import lib.fetch  # noqa: F401
import lib.rwfile  # noqa: F401
from lib.telegram import handle_message, reset, start


def main():
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        raise ValueError("TELEGRAM_BOT_TOKEN が設定されていません")

    telegram_app = Application.builder().token(telegram_token).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    telegram_app.add_handler(CommandHandler("reset", reset))

    telegram_app.run_polling(allowed_updates=Update.ALL_TYPES)


def make_memory_cache():
    memory_template_dir = Path("memory_template")
    memory_dir = Path("memory")
    if memory_dir.exists():
        shutil.rmtree(memory_dir)
    memory_dir.mkdir(exist_ok=True)
    for file in memory_template_dir.glob("*"):
        shutil.copy(file, memory_dir / file.name)


if __name__ == "__main__":
    make_memory_cache()
    main()
