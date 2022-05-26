from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer, Boolean, MetaData, ForeignKey, DateTime, Float

Base = declarative_base()


class Message(Base):
    """
    Таблица хранит в себе ID собщений, которые нужно удалить, чтобы не спамить
    сообщениями в интерфейсе
    """
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))


class User(Base):
    """
    Модель сущности "Пользователь"
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    chat_id = Column(Integer)

    is_admin = Column(Boolean, default=False)
    messages_for_delete = relationship(
        "Message", backref="messages_for_delete")
