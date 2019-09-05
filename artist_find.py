import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
	"""
	Описывает структуру таблицы album для хранения записей музыкальной бтблиотеки
	"""

	__tablename__ = "album"

	id = sa.Column(sa.INTEGER, primary_key=True)
	year = sa.Column(sa.INTEGER)
	artist = sa.Column(sa.TEXT)
	genre = sa.Column(sa.TEXT)
	album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
	"""
	Находит все альбомы в базе данных по заданному артисту
	"""
	session = connect_db()
	albums = session.query(Album).filter(Album.artist == artist).all()
	return albums

def find_album(album_data):
	"""
	Проверяет наличие альбома в БД
	"""
	artist = album_data["artist"]
	album = album_data["album"]
	session = connect_db()
	albums = len(session.query(Album).filter(Album.artist == artist).filter(Album.album == album).all())
	return albums

def add_album(album_data):
	"""
	Добавляет новый альбом в БД
	"""
	new_album = Album(year=album_data["year"], artist=album_data["artist"], genre=album_data["genre"], album=album_data["album"])
	session = connect_db()
	session.add(new_album)
	session.commit()
	return "Запись добавленна в БД"

def validation(album_data):
	"""
	Проверяет соответствие и пустоту полей
	"""
	year = album_data["year"]
	artist = album_data["artist"]
	genre = album_data["genre"]
	album = album_data["album"]
	if len(year)==4 and ((int(year[0])==1 and int(year[1])==9) or (int(year[0])==2 and int(year[1])==0)):
		if album and artist and genre:
			return True
		else:
			return False
	else:
		return False


