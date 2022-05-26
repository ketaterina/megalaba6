from datetime import datetime, timedelta

from .models import User
from config import MAIN_ADMIN_ID
from .mics import session, metadata, engine
from aiogram import types
from typing import List, Dict, Union
from mics import bot
from sqlalchemy import or_


class DataBaseFunc():
    """
    Класс для работы с базой данных. Содержит себе простейшию реализацую CRUD и вспомогательные функции по работе с БД
    """

    # region Инициализация БД и функции для отладки
    @staticmethod
    def add_main_admin() -> None:
        """Добавляет главного администратора при инициализации базы данных"""
        user = session.query(User).filter_by(id=MAIN_ADMIN_ID).first()
        if user == None:
            user = User(id=MAIN_ADMIN_ID, username="ketaterina",
                        is_admin=True)
            session.add(user)
            session.commit()
            return
        if user.is_admin == False:
            user.is_admin = True
            session.commit()
    # endregion

    # region Работа с классом User

    @staticmethod
    def get_user(param: Union[int, str], user_aio: types.User = None) -> User:
        """Возвращает объект пользователя из БД
        Args:
            param (Union[int, str]): Идентификатор пользователя или никнейм
            param (User): Объект пользователя aiogram
        Raises:
            Exception: Проверка на валидность типа переданных параметров
        Returns:
            User: Объект класса User
        """
        user = None
        if isinstance(param, int):
            user = session.query(User).filter_by(id=param).first()
        elif isinstance(param, str):
            user = session.query(User).filter_by(username=param).first()
        else:
            raise Exception("Неверный тип параметров")

        if not user and user_aio:
            user = User(id=user_aio.id, username=user_aio.username)
            DataBaseFunc.add(user)

        return user

    # endregion

    # region Работа с сообщениями

    @staticmethod
    async def delete_messages(user: User) -> None:
        """Удаляет ненужные сообщения пользователя."""
        for message in user.messages_for_delete:
            try:
                await bot.delete_message(chat_id=user.chat_id, message_id=message.message_id)
                session.delete(message)
                session.commit()
            except:
                pass

    @staticmethod
    async def delete_messages_from_callback(user: User, message_id: int) -> None:
        """Удаляет все сообщения, кроме тех, с которого была нажата кнопка"""
        for message in user.messages_for_delete:
            try:
                if (message.message_id == message_id):
                    continue
                await bot.delete_message(chat_id=user.chat_id, message_id=message.message_id)
                session.delete(message)
                session.commit()
            except:
                pass

    # endregion

    # region Базовые методы для базы данных

    @staticmethod
    def commit() -> None:
        """Сохраняет изменения в бд """
        session.commit()

    @staticmethod
    def add(obj=None) -> None:
        """Добавляет объект в базу данных"""
        if obj:
            session.add(obj)
            session.commit()
    # endregion

    @staticmethod
    def drop_all() -> None:
        """Удаляет БД"""
        metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)
