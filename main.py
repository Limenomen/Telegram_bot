import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, f"Привет, я бот. Чтобы посмотреть список команд - напишите /help")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, f"пока что тут пусто(")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, f"а я ничего и не понял, воспользуйся лучше командами - /help")


def main():
    bot.polling()
    pass


if __name__ == '__main__':
    main()
