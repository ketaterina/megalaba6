from tkinter import Button
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TEXTS, get_text
from database.models import User
from database.functions import DataBaseFunc
import re


class AdminGeneratorKeyboard():
    """Генерирует клавиатуру для админ меню"""
    @staticmethod
    async def get_add_admin(text):
        keyboard = InlineKeyboardMarkup()
        buttons = []

        users = DataBaseFunc.get_users_no_admin()

        for user in users:
            but = InlineKeyboardButton(user.username, callback_data=f"{text}_user@{user.id}")
            buttons.append(but)
        buttons.append(InlineKeyboardButton("Назад", callback_data="admin_menu_back_add_user"))
        keyboard.add(*buttons)
        return keyboard