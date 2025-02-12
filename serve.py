# serve.py
import logging
import os
from flask import Flask, request, jsonify
import telegram
from telegram import Bot

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

# 存储机器人信息的字典 (不适用于生产环境，仅用于演示)
# 格式: { "bot_name": chat_id }
bot_registry = {}

@app.route('/', methods=['GET'])
def index():
    return "Telegram Bot Server is running!"

@app.route('/register_bot', methods=['POST'])
def register_bot():
    """
    注册机器人，将机器人名称和 chat_id 关联起来。
    """
    try:
        data = request.get_json()
        bot_name = data.get('bot_name')
        chat_id = data.get('chat_id')

        if not bot_name or not chat_id:
            return jsonify({'status': 'error', 'message': 'bot_name and chat_id are required'}), 400

        bot_registry[bot_name] = chat_id
        logging.info(f"Registered bot: {bot_name} with chat_id: {chat_id}")

        return jsonify({'status': 'success', 'message': 'Bot registered successfully'})

    except Exception as e:
        logging.error(f"Error registering bot: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    """
    接收 POST 请求，发送消息到指定的 Telegram 机器人。
    """
    try:
        data = request.get_json()
        bot_name = data.get('bot_name')
        message = data.get('message')

        if not bot_name or not message:
            return jsonify({'status': 'error', 'message': 'bot_name and message are required'}), 400

        if bot_name not in bot_registry:
            return jsonify({'status': 'error', 'message': f'Bot {bot_name} is not registered'}), 404

        target_chat_id = bot_registry[bot_name]

        # 发送消息
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=target_chat_id, text=message)
        logging.info(f"Sent message: '{message}' to bot: {bot_name} (chat_id: {target_chat_id})")

        return jsonify({'status': 'success', 'message': 'Message sent successfully'})

    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
    logging.info("Telegram Bot Server started successfully!")
