from tkinter import Button
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TEXTS, get_text
from database.models import User
from database.functions import DataBaseFunc
import re


class UserGeneratorKeyboard():
    """Генерирует клавиатуру для пользователей"""
    @staticmethod
    async def get_keyboard_inline(user: User, text: str, row_wigth: int = 1,
                                  keyboard: InlineKeyboardMarkup = None, buttons: list = None) -> InlineKeyboardMarkup:
        """Генерирует клавиатуру по заданному ключу

        Args:
            user (User): Объект пользователя
            text (str): Ключ клавиатуры

        Returns:
            InlineKeyboardMarkup: Объект клавиатуры
        """
        if not keyboard:
            keyboard = InlineKeyboardMarkup()
        if not buttons:
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
    async def get_keyboard_add_song_to_album(user: User, text: str, row_wight: int = 1) -> InlineKeyboardMarkup:
        """Генерирует клавиатуру выбора песен по заданному ключу

        Args:
            user (User): Объект пользователя
            text (str): Ключ клавиатуры

        Returns:
            InlineKeyboardMarkup: Объект клавиатуры
        """
        songs = DataBaseFunc.get_all_songs()

        if not songs:
            return await UserGeneratorKeyboard.get_keyboard_inline(user, text)

        keyboard = InlineKeyboardMarkup()
        buttons = []

        for song in songs:
            but = InlineKeyboardButton(song.name, callback_data=f"{text}_&song@{song.id}")
            buttons.append(but)

        return await UserGeneratorKeyboard.get_keyboard_inline(user, text, row_wight, keyboard, buttons)


    @staticmethod
    async def get_keyboard_add_albums(user: User, text: str, row_wight: int = 1) -> InlineKeyboardMarkup:
        """Генерирует клавиатуру выбора альбомов по заданному ключу

        Args:
            user (User): Объект пользователя
            text (str): Ключ клавиатуры

        Returns:
            InlineKeyboardMarkup: Объект клавиатуры
        """
        song_id = int(re.search(pattern="song@\d+", string=text).group().replace('song@', ''))
        albums = DataBaseFunc.get_all_album_without_song(song_id)

        keyboard = InlineKeyboardMarkup()
        buttons = []

        for album in albums:
            but = InlineKeyboardButton(album.name, callback_data=f"{text}_&album@{album.id}")
            buttons.append(but)
        buttons.append(InlineKeyboardButton('Назад', callback_data='song_in_album_back'))
        keyboard.row_width = row_wight
        keyboard.add(*buttons)
        return keyboard


    @staticmethod
    def get_keyboard(*buttons):
        keyboard = InlineKeyboardMarkup()
        for but in buttons:
            keyboard.add(but)
        return keyboard
