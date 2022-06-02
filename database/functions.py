
from .models import Album, Song, User
from config import MAIN_ADMIN_ID
from .mics import session, metadata, engine
from aiogram import types
from typing import List, Dict, Text, Union
from mics import bot
from sqlalchemy import or_, select


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

    @staticmethod
    def get_users_no_admin() -> List[User]:
        return session.query(User).filter_by(is_admin=False).all()

    # endregion
    
    #region Работа с моделями данных для лабы
    def is_exist_song_name(text: str) -> bool:
        """
        Проверяет существование названия песни в БД
        :param text: Название песни
        :return: True, Если такое название уже существует
        """
        if not text or not isinstance(text, str):
            raise Exception(f"Ошибка валидации параметра: {text}")
        return bool(session.query(Song).filter_by(name=text).first())
    
    def is_exist_album_name(text: str) -> bool:
        """Проверяет существование названия альбома в БД

        Args:
            text (str): Название альбма

        Returns:
            bool: True, если существует
        """
        if not text or not isinstance(text, str):
            raise Exception(f"Ошибка валидации параметров при проверке сущетсвования альбома {text}")
        return bool(session.query(Album).filter_by(name=text).first())

    def add_song(text: str) -> None:
        """
        Добавляет новую песню в БД
        Args:
            text (str): Название песни
        """
        if not text or not isinstance(text, str):
            raise Exception(f"Ошибка валидации параметра: {text}")

        if DataBaseFunc.is_exist_song_name(text):
            raise Exception("Песня с таким названием уже существует")

        song = Song(name=text)
        DataBaseFunc.add(song)
    
    def add_album(text: str) -> None:
        """Добавляет новый альбом в БД

        Args:
            text (str): Название альбома
        """
        if not text or not isinstance(text, str):
            raise Exception(f"Ошибка валидации параметров при добавлении нового альбома {text}")
        
        if DataBaseFunc.is_exist_album_name(text):
            raise Exception("Альбом с таким названием уже существует")
        
        album = Album(name=text)
        DataBaseFunc.add(album)

    def get_all_songs() -> List[Song]:
        """Возвращает все песни из БД

        Returns:
            List[Song]: Список песен
        """
        return session.query(Song).all()
    
    def get_song(id: int) -> Song:
        """Возвращает объект класса Song по переданному идентификатору

        Args:
            id (int): Идентификатор песни

        Returns:
            Song: Объект класса Song из БД
        """
        if not id:
            return None
        
        return session.query(Song).filter_by(id=id).first()
    
    def get_album(id: int) -> Album:
        """Возвращает объект класса альбом

        Args:
            id (int): Идентификатор альбома

        Returns:
            Album: Объект класса альбом из БД
        """
        if not id:
            return None
        
        return session.query(Album).filter_by(id=id).first()
    
    def get_all_albums() -> List[Album]:
        """Возвращает все альбомы из БД

        Returns:
            List[Album]: Список альбомов
        """
        return session.query(Album).all()
    
    def get_all_album_without_song(song_id) -> List[Album]:
        """Возвращает все альбомы, в которых нет заданной песни

        Args:
            song_id (_type_): Идентификатор песни

        Returns:
            List[Album]: Список альбомов
        """
        if not song_id:
            return []
        
        albums = session.query(Album).all()
        song = session.query(Song).filter_by(id=song_id).first()
        song_albums_id = [item.id for item in song.albums]
        
        return [album for album in albums if album.id not in song_albums_id]
    #endregion

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
