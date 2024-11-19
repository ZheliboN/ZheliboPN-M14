
import sqlite3
import os

DB_NAME = 'products.db'
DEFAULT_BALANCE = 1000

# Если файл базы данных отсутствует, то создаем его
if not os.path.isfile(DB_NAME):
    f = open(DB_NAME, 'w')
    f.close()
# Подключаемся к файлу базы данных
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()


def initiate_db():
    # Если в базе данных нет таблицы Products, то создаем её
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    # Добавляем в таблицу сведения (записи) о продуктах
    for number in range(1, 5):
        # Для исключения дублирования записей, проверяем наличие такого же товара в таблице
        cursor.execute('SELECT id, title, description, price FROM Products WHERE title = ?', (f'Продукт {number}',))
        products = cursor.fetchall()
        # Добавляем новую запись о товаре только в том случае, если такого товара нет в таблице
        if len(products) == 0:
            cursor.execute(
                'INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                (f'Продукт {number}', f'Описание {number}', number * 100)
                          )
            connection.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')
    connection.commit()


def is_included(username):
    result = True
    check_user = cursor.execute('SELECT username FROM Users WHERE username = ?', (username,))
    if check_user.fetchone() is None:
        result = False
    connection.commit()
    return result


def add_user(username, email, age):
    if not is_included(username):
        cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)',
                       (username, email, age, DEFAULT_BALANCE))
        connection.commit()


# Получаем список всех записей из таблицы
def get_all_products():
    cursor.execute('SELECT id, title, description, price FROM Products')
    data_base = cursor.fetchall()
    connection.commit()
    connection.close()
    return list(data_base)

initiate_db()
