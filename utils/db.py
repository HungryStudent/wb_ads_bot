from contextlib import closing
from datetime import datetime, time, date
from sqlite3 import Cursor
import sqlite3

database = "utils/database.db"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users(user_id INT, username TEXT, first_name TEXT, city INT, gender INT, reg_time INT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS cities(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, code TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS catalog(serial_id INTEGER PRIMARY KEY AUTOINCREMENT, id INTEGER, name TEXT, parent_id INTEGER, url TEXT)")
        connection.commit()


def get_users():
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users")
        return cursor.fetchall()


def get_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute(
            "SELECT user_id, cities.name, cities.code as city_code, gender FROM users join cities on cities.id = users.city WHERE user_id = ?",
            (user_id,))
        return cursor.fetchone()


def get_cities():
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM cities")
        return cursor.fetchall()


def add_user(user_id, username, first_name):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, 1, 0, ?)",
                       (user_id, username, first_name, int(datetime.now().timestamp())))
        connection.commit()


def change_gender(user_id, gender_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("UPDATE users SET gender = ? WHERE user_id = ?", (gender_id, user_id))
        connection.commit()


def change_city(user_id, city_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("UPDATE users SET city = ? WHERE user_id = ?", (city_id, user_id))
        connection.commit()


def get_category(category_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM categories WHERE id = ?", (category_id,))
        return cursor.fetchone()


def get_catalog():
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM catalog WHERE parent_id = 0 ORDER BY serial_id")
        return cursor.fetchall()


def get_catalog_childs(catalog_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM catalog WHERE parent_id = ? ORDER BY serial_id", (catalog_id,))
        return cursor.fetchall()


def get_catalog_by_id(catalog_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT id, name, url FROM catalog WHERE id = ?", (catalog_id,))
        return cursor.fetchone()


def get_stat():
    end = int(datetime.now().timestamp())
    start = int(datetime.combine(date.today(), time()).timestamp())
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        cursor.execute("SELECT (SELECT COUNT() FROM users) as users_count,"
                       "(SELECT COUNT() FROM users where reg_time between ? and ?) as today_users_count",
                       (start, end))
        return cursor.fetchone()
