import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from lib.state import AppState
from lib.telegram import handle_message, reset, start


def main():
    print("起動中...")
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


if __name__ == "__main__":
    print("set_agent")
    AppState.set_agent()
    print("init_notes_dir")
    AppState.init_notes_dir()
    main()
