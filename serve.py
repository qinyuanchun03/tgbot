# serve.py
import logging
import os
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 导入 config.py
try:
    import config
    TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
    logging.info("Successfully imported config.py")
except ImportError as e:
    logging.error(f"ImportError: Could not import config.py: {e}")
    exit(1)
except AttributeError as e:
    logging.error(f"AttributeError: Missing attribute in config.py: {e}")
    exit(1)

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 创建 Flask 应用
app = Flask(__name__)

# 存储 CHAT_ID 的字典 (不适用于生产环境，仅用于演示)
chat_ids = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令."""
    chat_id = update.effective_chat.id
    chat_ids[chat_id] = True  # 存储 CHAT_ID
    logging.info(f"Registered CHAT_ID: {chat_id} for user: {update.effective_user.username}")
    await context.bot.send_message(chat_id=chat_id, text="已注册，可以接收消息了！")

@app.route('/', methods=['GET'])
def index():
    return "Telegram Bot Server is running!"

@app.route('/send_message', methods=['POST'])
def send_message():
    """
    接收 POST 请求，发送消息到 Telegram 聊天。
    """
    try:
        data = request.get_json()
        message = data.get('message')
        target_chat_id = data.get('chat_id')  # 从请求中获取 chat_id

        if not message:
            return jsonify({'status': 'error', 'message': 'Message is required'}), 400

        if not target_chat_id:
            return jsonify({'status': 'error', 'message': 'chat_id is required'}), 400

        target_chat_id = int(target_chat_id)  # 转换为整数

        if target_chat_id not in chat_ids:
            return jsonify({'status': 'error', 'message': 'chat_id is not registered'}), 403

        # 发送消息
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=target_chat_id, text=message)
        logging.info(f"Sent message: '{message}' to chat ID: {target_chat_id}")

        return jsonify({'status': 'success', 'message': 'Message sent successfully'})

    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 启动 Telegram Bot 监听器
def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()

if __name__ == '__main__':
    # 启动 Telegram Bot 监听器 (在单独的线程中)
    import threading
    telegram_thread = threading.Thread(target=run_telegram_bot)
    telegram_thread.start()

    # 启动 Flask 应用
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
    logging.info("Telegram Bot Server started successfully!")
