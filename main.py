import os
from collections import defaultdict

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv(".env")
api_key = os.getenv("GROQ_API_KEY")

model = GroqModel(
    "llama-3.3-70b-versatile",
    provider=GroqProvider(api_key=api_key),
)

agent = Agent(model, instructions="日本語で解答してください。")

histories: defaultdict[int, list[ModelMessage]] = defaultdict(list)


# --- Telegram ハンドラー ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    histories[update.effective_chat.id].clear()
    await update.message.reply_text("こんにちは！何でも聞いてください。")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    chat_id = update.effective_chat.id
    user_text = update.message.text

    if user_text is None:
        return

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    result = await agent.run(
        user_text,
        message_history=histories[chat_id],
    )

    histories[chat_id] = result.all_messages()

    await update.message.reply_text(result.output)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    histories[update.effective_chat.id].clear()
    await update.message.reply_text("会話履歴をリセットしました。")


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


if __name__ == "__main__":
    main()
