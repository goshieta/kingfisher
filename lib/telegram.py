from telegram import Update
from telegram.ext import ContextTypes

from lib.state import AppState


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    AppState.histories[update.effective_chat.id].clear()
    await update.message.reply_text("こんにちは！何でも聞いてください。")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    chat_id = update.effective_chat.id
    user_text = update.message.text

    if user_text is None:
        return

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    result = await AppState.agent.run(
        user_text,
        message_history=AppState.histories[chat_id],
    )

    AppState.histories[chat_id] = result.all_messages()

    await update.message.reply_text(result.output)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    AppState.histories[update.effective_chat.id].clear()
    await update.message.reply_text("会話履歴をリセットしました。")
