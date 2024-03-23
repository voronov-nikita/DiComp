# 
# Файл основной логики хранения данных польхователей
# В файле работа происзодит в основном с использованием библиотеки sqlite3, встроенной в python
# База данных является релиационной, и хранит в себе информацию обо всем: данные пользователей, теущие ссесии, задачи и разрешения 
# 


import sqlite3 as sql



# исходный файл базы данных
FILE_DATABASE:str = "data.db"



# <------------------------------- Функции, используемые в глобальном представлении -------------->

def checkLogin(login:str, password:str) -> bool:
    '''
    
    '''
    
    db = sql.connect(FILE_DATABASE)
    cursor = db.cursor()
    
    cursor.execute(
        f"""SELECT * FROM users WHERE login='{login}'"""
    )
    
    return password in cursor.fetchone()


def addNewUser(login:str, email:str, password:str) -> bool:
    '''
    
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


def _checkCorrectLogin(login:str):
    '''
    
    '''
    
    db = sql.connect(FILE_DATABASE)
    cursor = db.cursor()
    
    cursor.execute(
        f"""SELECT * FROM users WHERE login='{login}'"""
    )
    
    return cursor.fetchone()


if __name__=="__main__":
    _createDatabaseUsers()
    # тестируем добавление пользователя
    addNewUser(login="test", email="test@test.ru", password="1234567890")
