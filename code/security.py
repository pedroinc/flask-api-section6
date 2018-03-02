import sqlite3

from user import User

connection = sqlite3.connect('../data.db')
cursor = connection.cursor()

query_by_id = "select * from users where id = ?"
query_by_name = "select * from users where username = ?"

username_mapping = { u.username: u for u in cursor.execute(query_by_name) }
userid_mapping = { u.id: u for u in cursor.execute(query_by_id) }

connection.close()

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
