# utils/menu.py
from telegram import ReplyKeyboardMarkup

def generate_main_menu():
    """生成主菜单."""
    keyboard = [
        ["作者信息", "绑定我的邮箱"],
        ["作者推荐的VPN", "调用大模型"],
        ["菜单"]  # 保留 "菜单" 选项
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
