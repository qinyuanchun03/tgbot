# bot.py
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from config import TELEGRAM_BOT_TOKEN
from utils.menu import generate_main_menu
from commands import start, help_command  # 导入命令处理模块

# 启用日志记录
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 定义状态
EMAIL_INPUT = 1

# 定义全局变量
user_emails = {}  # 用于存储用户邮箱

async def author_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 "作者信息" 选项."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="江湖笔者机器人@江湖笔者制作，是一个简易好用的机器人"
    )

async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """询问用户邮箱."""
    await update.message.reply_text("请输入你的邮箱地址：")
    return EMAIL_INPUT

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """获取用户邮箱并记录."""
    user_email = update.message.text
    user_id = update.message.from_user.id
    user_emails[user_id] = user_email  # 存储邮箱
    await update.message.reply_text(f"已记录你的邮箱：{user_email}")
    return ConversationHandler.END

async def author_vpn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 "作者推荐的VPN" 选项."""
    vpn_link = "https://example.com/vpn"  # 替换为你的 VPN 链接
    vpn_description = "这是一个作者推荐的 VPN，速度快，安全可靠。"  # 替换为你的 VPN 说明
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"推荐 VPN：{vpn_link}\n\n{vpn_description}"
    )

async def call_llm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 "调用大模型" 选项."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="正在调用大模型，请稍候..."
    )
    # 在这里添加调用大模型的代码
    # 例如，可以使用 OpenAI API 或其他 API
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="大模型调用完成！"  # 替换为大模型的输出
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理用户发送的消息."""
    user_message = update.message.text
    user_id = update.message.from_user.id

    # 在这里添加你的消息处理逻辑
    # 例如，可以根据消息内容调用不同的函数
    if user_message == "菜单":
        await send_menu(update, context)
    elif user_message == "作者信息":
        await author_info(update, context)
    elif user_message == "绑定我的邮箱":
        return await ask_email(update, context)  # 进入对话状态
    elif user_message == "作者推荐的VPN":
        await author_vpn(update, context)
    elif user_message == "调用大模型":
        await call_llm(update, context)
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
    application.add_handler(CommandHandler("help", help_command))

    # 创建对话处理程序
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],  # 对话入口
        states={
            EMAIL_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],  # 获取邮箱状态
        },
        fallbacks=[],  # 没有回退处理程序
    )
    # 添加对话处理程序
    #application.add_handler(conv_handler)

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
