import sqlite3
from sqlite3 import Error


def sql_query(query):
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Error as e:
            print(e)
        result = cursor.fetchall()
        return result


def create_tables():
    users_query = """CREATE TABLE IF NOT EXISTS users 
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        user_name TEXT
                        name TEXT);"""
    tasks_query = """CREATE TABLE IF NOT EXISTS tasks 
                        (task_id INTEGER PRIMARY KEY NOT NULL,
                        task_name TEXT,
                        task_date TEXT,
                        user_id INTEGER FOREIGN KEY (fk_user_id) REFERENCES users (user_id);"""
    sql_query(users_query)
    sql_query(tasks_query)


def add_user(user_id, user_name, name):
    user_exist = sql_query(f"SELECT FROM users WHERE user_id = {user_id}")
    if not user_exist:
        insert_user_query = f'INSERT INTO users (user_id, user_name, name) \
                            VALUES ({user_id}, "{user_name}", "{name}");'
        sql_query(insert_user_query)


def add_task(user_id, task_name, task_date):
    insert_task_query = f'INSERT INTO tasks (task_id, task_name, task_date, user_id)\
                        VALUES (Null, "{task_name}", "{task_date}", {user_id});'
    sql_query(insert_task_query)
