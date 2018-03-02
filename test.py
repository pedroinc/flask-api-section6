import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table_users = "create table users(id int, username text, password text)"
cursor.execute(create_table_users)

user = (1, 'pedro', 'ph77')
insert_query = "insert into users values (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'joao', 'ab09'),
    (3, 'jose', 'cf10')
]

cursor.executemany(insert_query, users)

select_query = "select * from users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
