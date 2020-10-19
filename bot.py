import telebot
import os

from telebot import types

AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
MEDIA_PATH = os.environ.get("MEDIA_PATH")

bot = telebot.TeleBot(AUTH_TOKEN)

@bot.message_handler(commands=['start'])
def getStarted(message):
    #creating keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/help")
    item2 = types.KeyboardButton("...")
    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Давай начнём! Используй команду /help для большей информации".
    format(message.from_user, bot.get_me()), parse_mode='html',
    reply_markup=markup)

@bot.message_handler(content_types=["document"])
def download(message):
    chat_id = message.chat.id

    file_infos = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_infos.file_path)

    src = MEDIA_PATH + message.from_user.username + '.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Спасибо, фотограифия была добавлена")

bot.polling(none_stop=True)