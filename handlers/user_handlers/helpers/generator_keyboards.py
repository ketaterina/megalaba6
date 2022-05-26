from tkinter import Button
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TEXTS, get_text
from database.models import User
from database.functions import DataBaseFunc


class UserGeneratorKeyboard():
    """Генерирует клавиатуру для пользователей""" 
    @staticmethod
    async def get_keyboard_inline(user: User, text: str, row_wigth: int = 1) -> InlineKeyboardMarkup:
        """Генерирует клавиатуру по заданному ключу

        Args:
            user (User): Объект пользователя
            text (str): Ключ клавиатуры

        Returns:
            InlineKeyboardMarkup: Объект клавиатуры
        """
        keyboard = InlineKeyboardMarkup()
        buttons = []
        
        for key, value in get_text(text, True).items():
            if "admin" in key and not user.is_admin:
                continue

            but = InlineKeyboardButton(value, callback_data=f"{text}_{key}")
            buttons.append(but)

        keyboard.row_width = row_wigth
        keyboard.add(*buttons)
        return keyboard

    @staticmethod
    def get_keyboard(*buttons):
        keyboard = InlineKeyboardMarkup()
        for but in buttons:
            keyboard.add(but)
        return keyboard
