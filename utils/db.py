import psycopg2
from typing import List
from os import getenv
from dotenv import load_dotenv


class DB(object):

    _ADDRESS = None
    _PORT = None
    _LOGIN = None
    _PASSWORD = None
    _DBNAME = None
    def __init__(self, **kwargs) -> None:
        self._ADDRESS = getenv("address")
        self._PORT = getenv("port")
        self._LOGIN = getenv("login")
        self._PASSWORD = getenv("password")
        self._DBNAME = getenv("dbname")

        if (self._PASSWORD is None or self._PORT is None or self._LOGIN is None or self._PASSWORD is None):
            raise ValueError("Отсутствуют данные для подключения к БД")
        
        self._conn = psycopg2.connect(
            host=self._ADDRESS,
            port=self._PORT,
            user=self._LOGIN,
            password=self._PASSWORD,
            dbname=self._DBNAME
        )

    def add_user(self, id_telegram: int, username: str) -> None:
        """
        Добавление пользователя через процедуру SQL.
        @param int id_telegram: id пользователя которого нужно добавить.
        @param str username: псевдоним пользователя в телеграм.
        """
        try:
            with self._conn.cursor() as cursor:
                cursor.callproc('users.add_user_auth', [id_telegram, username])
                self._conn.commit()
        except Exception as e:
            self._conn.rollback()
        finally:
            self._conn.close()

    def accept_request(self, user_id: int):
        """
        Добавление метки доступа для пользователя.
        @param int user_id: id пользователя получающего метку.
        """
        try:
            with self._conn.cursor() as cursor:
                cursor.callproc('users.accept_request', [user_id])
                self._conn.commit()
        except Exception as e:
            self._conn.rollback()
        finally:
            self._conn.close()
        
    def add_user_photo(self, id_telegram: int, photo_path: str) -> None:
        """
        Добавление пути к фотографии к пользователю.
        @param int id_telegram: id пользователя добавляющего фотографию.
        @param str photo_path: Путь к фотографии.
        """
        try:
            with self._conn.cursor() as cursor:
                cursor.callproc('users.insert_photo', [id_telegram, photo_path])
                self._conn.commit()
        except Exception as e:
            self._conn.rollback()
        finally:
            self._conn.close()

    def get_user_photos(self, id_telegram: int) -> List:
        """
        Получение списка путей к фотографиям пользователя.
        @param int id_telegram: id пользователя фотографий.
        """
        try:
            with self._conn.cursor() as cursor:
                cursor.callproc('users.get_photos', [id_telegram])
                photos = cursor.fetchall()
                return [photo[0] for photo in photos]
        except Exception as e:
            return []
        finally:
            self._conn.close()

if __name__ == "__main__":
    db = DB()
    db.add_user(2, "testuser")
    db.accept_request(2)
    db.add_user_photo(2, "http://example.com/photo.jpg")
    db.get_user_photos(2)