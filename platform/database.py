#
# Файл основной логики хранения данных польхователей
# В файле работа происзодит в основном с использованием библиотеки sqlite3, встроенной в python
# База данных является релиационной, и хранит в себе информацию обо всем: данные пользователей, теущие ссесии, задачи и разрешения
#


import sqlite3 as sql


# исходный файл базы данных
FILE_DATABASE: str = "data.db"


# <------------------------------- Функции, используемые в глобальном представлении -------------->

def checkLogin(login: str, password: str) -> bool:
    '''
    Проверка соответствия логина и пароля. 

    Создается запрос к базе данных пользователей и 
    сравнивается полученные пароль с указанным в БД и возвращается булевое значение True/False.
    '''

    db = sql.connect(FILE_DATABASE)
    cursor = db.cursor()

    cursor.execute(
        f"""SELECT password FROM users WHERE login='{login}'"""
    )
    try:
        return password in cursor.fetchone()
    except TypeError:
        return False


def addNewUser(login: str, email: str, password: str) -> bool:
    '''
    Добавление нового пользователя в БД.

    Создается запрос на добавление в таблицу пользователей новых данных. 
    Для этого необходимо передать новые данные: 
    - уникальный логин пользователя (логин проверяется на совпадение)
    - электронная почта пользователя для получения последующих рассылок
    - пароль пользователя для авторизации в системе


    '''

    if _checkCorrectLogin(login):
        return False

    db = sql.connect(FILE_DATABASE)
    cursor = db.cursor()

    cursor.execute(
        f"""INSERT INTO users(login, email, password) VALUES('{login}', '{email}', '{password}')
    """
    )

    # сохраняем
    db.commit()
    db.close()

    return True


# <---------------- Исключительно локальные функции -------------------->

def _createDatabaseUsers() -> None:
    '''
    Создается локальная база данных формата sqlite3, хранящая в себе информацию о зарегестрированых и тестовых пользователях.
    '''

    db = sql.connect(FILE_DATABASE)
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    db.commit()
    db.close()


def _checkCorrectLogin(login: str) -> tuple:
    '''
    Проверка логина на совпадение. Так как логин должен быть уникальным, то
    необходимо при регистрации проверять наличие такого же логина в БД.

    Возвращается кортеж данных, пустой если логин свободен.
    '''

    db = sql.connect(FILE_DATABASE)
    cursor = db.cursor()

    cursor.execute(
        f"""SELECT * FROM users WHERE login='{login}'"""
    )

    return cursor.fetchone()


if __name__ == "__main__":
    _createDatabaseUsers()
    # тестируем добавление пользователя
    addNewUser(login="test", email="test@test.ru", password="1234567890")
