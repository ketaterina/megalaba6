import os
import json
import logging


TOKEN = "5357378358:AAG3WLF0iWixuAFVZQckedpP3XsZl1XAQao"
MAIN_ADMIN_ID = 465526719

texts_filename = "texts//texts.json"
texts_but_filename = "texts//texts_button.json"

TEXTS = {}
TEXTS_BUTTON = {}
DELEMITER = "&"

def add_button_back(text: dict):
    for _, value in text.items():
        value['&back'] = "Назад"

try:
    with open(texts_filename, 'r', encoding='utf8') as file:
        TEXTS = json.load(file)

    with open(texts_but_filename, 'r', encoding='utf8') as file:
        TEXTS_BUTTON = json.load(file)
        add_button_back(TEXTS_BUTTON)
except Exception as exc:
    logging.error(str(exc))


def get_text(text: str, is_button: bool = False) -> str:
    """Возвращает текст сообщений пользователя или кнопок

    Args:
        text (str): Идентификатор текста в JSON файле
        is_button (bool): Флаг для возврата текста кнопки

    Returns:
        str: Текст для кнопки или сообщения пользователю
    """
    if not is_button:
        return TEXTS[text] if text in TEXTS else "Текст не придумали"
    return TEXTS_BUTTON[text] if text in TEXTS_BUTTON else {}
