import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# for i in range(1, 11):
# формируем запрос на выборку по имени пользователя, которого планирем добавить в таблицу
#     cursor.execute('SELECT username, email, age, balance FROM Users WHERE username = ?', (f'User{i}',))
#     users = cursor.fetchall()
# добавляем пользователя с текущим именем, только если его нет в базе данных (для избежания дублирования),
# т.е. добавляем только если в выборке из существующей базы данных 0 пользователей с заданным именем
#     if len(users) == 0:
#         cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)',
#                        (f'User{i}', f'example{i}@gmail.com', i*10, 1000))

# изменяем balance каждлго 2-го на 500
# for i in range(1, 11, 2):
#    cursor.execute('UPDATE Users SET balance =? WHERE username = ?', (500, f'User{i}'))

# удаляем каждого 3-го, начиная с 1-го
# for i in range(1, 11, 3):
#     cursor.execute('DELETE FROM Users WHERE username = ?', (f'User{i}',))

# вывод в консоль всех пользователей (результат по задаче module_14_1)
# cursor.execute('SELECT * FROM Users WHERE age != 60')
# users = cursor.fetchall()
# for user in users:
#     print(f'Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}')

# удаление пользователя с id = 6
cursor.execute('DELETE FROM Users WHERE id = ?', (6,))
connection.commit()

# подсчет количества пользователей
cursor.execute('SELECT COUNT(*) FROM Users')
count_user = cursor.fetchone()[0]
print(f'Количество всех пользователей: {count_user}')

# подсчет суммы всех балансов
cursor.execute('SELECT SUM(balance) FROM Users')
summ_all_balance = cursor.fetchone()[0]
print(f'Cумма всех балансов: {summ_all_balance}')

print(f'Средний баланс всех пользователей: {summ_all_balance/count_user}')

connection.close()
