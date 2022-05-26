"""Вспомогательные функции для работы с пользовательским меню"""
from config import DELEMITER


def get_call_data(text: str) -> str:
    """Удаляет из callback.data разделители кнопок для получения клавиатуры и следующег текста. 
    Если это кнопка назад удалят 2 разделителя с целью вернутся к изначальному состоянию
    Args:
        text (str): Описание callback.data
    Returns:
        str: Новый callback.data
    """
    index_delimiters = [index for index, value in enumerate(text) if value == DELEMITER]
    is_odd = len(index_delimiters) % 2 == 0

    if not index_delimiters:
        pass

    if is_odd and 'back' in text and index_delimiters:
        delete_indexs = sorted(index_delimiters[-2:])
        return text[:delete_indexs[0] - 1]

    return text