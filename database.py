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
        cursor.close()
        return result


def create_tables():
    users_query = '''CREATE TABLE IF NOT EXISTS users 
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        user_name TEXT,
                        name TEXT);'''
    tasks_query = '''CREATE TABLE IF NOT EXISTS tasks 
                        (task_id INTEGER PRIMARY KEY NOT NULL,
                        task_name TEXT,
                        task_date TEXT,
                        user_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users (user_id));'''
    sql_query(users_query)
    sql_query(tasks_query)


def user_exist(user_id):
    exist = sql_query(f'SELECT * FROM users WHERE user_id = {user_id}')
    return exist


def task_exist(user_id):
    exist = sql_query(f'SELECT * FROM tasks WHERE user_id = {user_id}')
    return exist


def add_user(user_id, user_name, name):
    if not user_exist(user_id):
        insert_user_query = f'INSERT INTO users (user_id, user_name, name)' \
                            f'VALUES ({user_id}, "{user_name}", "{name}");'
        sql_query(insert_user_query)


def add_task(user_id, task_name, task_date):
    insert_task_query = f'INSERT INTO tasks (task_id, task_name, task_date, user_id)'\
                        f'VALUES (Null, "{task_name}", "{task_date}", {user_id});'
    sql_query(insert_task_query)


def get_task_for_user(user_id):
    get_query = f'SELECT * FROM tasks WHERE user_id = {user_id}'
    return sql_query(get_query)


def delete_task(task_id):
    delete_query = f'DELETE FROM tasks WHERE task_id = {task_id}'
    sql_query(delete_query)


def check_all_users():
    check_all_query = f'SELECT * FROM users'
    return sql_query(check_all_query)


def check_all_tasks():
    check_all_query = f'SELECT * FROM tasks'
    return sql_query(check_all_query)
