import telebot
from telebot import types
import database
from config import TOKEN
from datetime import datetime
from threading import Thread
from time import sleep

bot = telebot.TeleBot(TOKEN)
database.create_tables()
#database.check_all_users()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, f"Привет, я бот. Чтобы посмотреть список команд - напишите /help")


@bot.message_handler(commands=['help'])
def send_help(message):
    register_button = types.InlineKeyboardButton('регистрация', callback_data='register')
    add_task_button = types.InlineKeyboardButton('добавить задачу', callback_data='add_task')
    delete_task_button = types.InlineKeyboardButton('удалить задачу', callback_data='delete_task')
    if not database.user_exist(message.from_user.id):
        buttons = types.InlineKeyboardMarkup().add(register_button)
        bot.send_message(message.from_user.id, f"Доступные команды:", reply_markup=buttons)

    elif not database.task_exist(message.from_user.id):
        buttons = types.InlineKeyboardMarkup().add(add_task_button)
        bot.send_message(message.from_user.id, f"Доступные команды:", reply_markup=buttons)

    else:
        buttons = types.InlineKeyboardMarkup().add(add_task_button, delete_task_button)
        bot.send_message(message.from_user.id, f"Доступные команды:", reply_markup=buttons)


@bot.callback_query_handler(func=lambda call: call.data == 'register')
def register_user(call):
    ask_a_question = bot.send_message(call.from_user.id, f"Как мне к вам обращаться?")
    bot.register_next_step_handler(ask_a_question, get_name)


def get_name(message):
    name = message.text
    database.add_user(message.from_user.id, message.from_user.username, name)
    bot.send_message(message.from_user.id, "Готово, теперь можно планировать задачи.")
    send_help(message)


@bot.callback_query_handler(func=lambda call: call.data == 'add_task')
def get_task(call):
    ask_a_question = bot.send_message(call.from_user.id, f"Введите название задания")
    bot.register_next_step_handler(ask_a_question, get_task_name)


def get_task_name(message):
    task_name = message.text
    ask_a_question = bot.send_message(message.from_user.id, f"Введите дату и время напоминания в следующем формате: день-месяц-год часы.минуты")
    bot.register_next_step_handler(ask_a_question, get_task_time, task_name)


def get_task_time(message, task_name):
    try:
        task_date = message.text
        datetime.strptime(task_date, "%d-%m-%Y %H.%M").strftime("%d-%m-%Y %H:%M")
        register_task(message, task_name, task_date)
    except Exception as e:
        ask_a_question = bot.send_message(message.from_user.id, f"Возможно неверный ввод, попробуйте еще раз.")
        bot.register_next_step_handler(ask_a_question, get_task_time, task_name)
        print(e)


def register_task(message, task_name, task_date):
    database.add_task(message.from_user.id, task_name, task_date)
    bot.send_message(message.from_user.id, f"Готово, я обязательно вам об этом напомню.")
    send_help(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, f"A я ничего и не понял, воспользуйтесь лучше командами - /help")


def make_dict(data):
    keys = ('task_id', 'task_name', 'task_date', 'user_id')
    for index in range(len(data)):
        data[index] = dict(zip(keys, data[index]))
    return data


def task_search():
    while True:
        data = database.check_all_tasks()
        tasks = make_dict(data)
        now = datetime.now()
        if tasks:
            for task in tasks:
                task_date = datetime.strptime(task['task_date'], "%d-%m-%Y %H.%M")
                if task_date.hour == now.hour and task_date.minute == now.minute:
                    bot.send_message(task['user_id'], f"Напоминаю, сейчас {task['task_name']}!")
        sleep(60)


def main():
    task_search_thread = Thread(target=task_search, daemon=True)
    task_search_thread.start()
    bot.polling()
    pass


if __name__ == '__main__':
    main()
