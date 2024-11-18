
import sqlite3
import os

DB_NAME = 'products.db'


def initiate_db():
    # Если файл базы данных отсутствует, то создаем его
    if not os.path.isfile(DB_NAME):
        f = open(DB_NAME, 'w')
        f.close()
    # Подключаемся к файлу базы данных
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
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
    connection.close()


# Получаем список всех записей из таблицы
def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, title, description, price FROM Products')
    data_base = cursor.fetchall()
    connection.commit()
    connection.close()
    return list(data_base)
