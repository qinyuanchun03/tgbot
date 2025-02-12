# commands/help.py
from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是一个帮助信息。")
