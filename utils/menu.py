# utils/menu.py
from telegram import ReplyKeyboardMarkup

def generate_main_menu():
    """生成主菜单."""
    keyboard = [
        ["选项 1", "选项 2"],
        ["选项 3", "菜单"]  # 添加 "菜单" 选项
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
