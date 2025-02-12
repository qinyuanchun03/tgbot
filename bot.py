# bot.py
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from utils.menu import generate_main_menu
from commands import start, help  # 导入命令处理模块

# 启用日志记录
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理用户发送的消息."""
    user_message = update.message.text
    user_id = update.message.from_user.id

    # 在这里添加你的消息处理逻辑
    # 例如，可以根据消息内容调用不同的函数
    if user_message == "菜单":
        await send_menu(update, context)
    else:
        await update.message.reply_text(f"你发送了: {user_message}")


async def send_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """发送主菜单."""
    menu_keyboard = generate_main_menu()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="请选择一个选项:",
        reply_markup=menu_keyboard
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理未知命令."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="抱歉，我不明白这个命令。")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """错误处理程序."""
    logging.error(f"Update {update} caused error {context.error}")


def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # 添加命令处理程序
    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("help", help.help_command))

    # 添加消息处理程序
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 添加未知命令处理程序
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # 添加错误处理程序
    application.add_error_handler(error_handler)

    # 启动机器人
    application.run_polling()


if __name__ == '__main__':
    main()
