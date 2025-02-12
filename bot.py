# bot.py
import logging
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 导入 config.py
try:
    import config
    logging.info("Successfully imported config.py")
except ImportError as e:
    logging.error(f"ImportError: Could not import config.py: {e}")
    exit(1)

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 调试输出
logging.info(f"Current working directory: {os.getcwd()}")

try:
    logging.info(f"Contents of commands directory: {os.listdir('commands')}")
except FileNotFoundError:
    logging.error("commands directory not found!")
    exit(1)  # 退出程序，因为 commands 目录是必需的
except Exception as e:
    logging.error(f"Error listing commands directory: {e}")
    exit(1)

try:
    from commands import start, help_command  # 导入命令处理模块
    logging.info("Successfully imported start and help_command from commands")
except ImportError as e:
    logging.error(f"ImportError: {e}")
    exit(1)  # 退出程序，因为导入失败

# 你的 Bot Token (从 config.py 获取)
try:
    TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
    logging.info("Successfully loaded TELEGRAM_BOT_TOKEN from config.py")
except AttributeError:
    logging.error("TELEGRAM_BOT_TOKEN not found in config.py!")
    exit(1)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)  # 直接使用 start 函数
    help_handler = CommandHandler('help', help_command)
    hello_handler = CommandHandler('hello', hello)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(hello_handler)

    logging.info("Bot started successfully!")
    application.run_polling()
