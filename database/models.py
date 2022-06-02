from email.mime import base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer, Boolean, MetaData, ForeignKey, DateTime, Float, Date

Base = declarative_base()

association_table = Table(
    "songs_album",
    Base.metadata,
    Column("song_id", ForeignKey("songs.id")),
    Column("album_id", ForeignKey("albums.id")),
)


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

class Album(Base):
    """
    Модель сущности "Альбом"
    """
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    date = Column(Date)
    songs = relationship(
        "Song", secondary=association_table, back_populates="albums"
    )


class Group(Base):
    """
    Модель сущности "Группа"
    """
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    songs = relationship("Song", back_populates="group")


class Song(Base):
    """
    Модель сущности "Песня"
    """
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    albums = relationship(
        "Album", secondary=association_table, back_populates="songs"
    )
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="songs")


