# commands/start.py
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="欢迎使用我的机器人！")
    # 发送菜单
    from utils.menu import generate_main_menu
    menu_keyboard = generate_main_menu()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="请选择一个选项:",
        reply_markup=menu_keyboard
    )


# commands/help.py
from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是一个帮助信息。")
