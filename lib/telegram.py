import shutil
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from lib.state import AppState


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    AppState.histories[update.effective_chat.id].clear()
    make_memory_cache()

    chat_id = update.effective_chat.id
    startup_message = Path("prompt/startup.md").read_text(encoding="UTF-8")

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    result = await AppState.agent.run(
        startup_message,
        message_history=AppState.histories[chat_id],
    )

    AppState.histories[chat_id] = result.all_messages()

    await update.message.reply_text(result.output)


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


def make_memory_cache():
    print("メモリコピー開始")
    memory_template_dir = Path("memory_template")
    memory_dir = Path("memory")
    if memory_dir.exists():
        shutil.rmtree(memory_dir)
    memory_dir.mkdir(exist_ok=True)
    shutil.copytree(memory_template_dir, memory_dir, dirs_exist_ok=True)
    print("メモリコピー完了")
