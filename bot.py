import telebot
import os
import datetime

from datetime import datetime, date, time
from telebot import types

AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
#MEDIA_PATH = os.environ.get("MEDIA_PATH")

bot = telebot.TeleBot(AUTH_TOKEN)

def dayOfWeek():
    return datetime.today().weekday()

#Parsing format
def parseFromat(line):
    line, ext = os.path.splitext(line)
    if ext == ".png":
        return 1
    elif ext == ".jpg":
        return 1
    elif ext == ".PNG":
        return 1
    elif ext == ".JPG":
        return 1
    elif ext == ".JPEG":
        return 1
    else:
        return 0

@bot.message_handler(commands=['start'])
def getStarted(message):
    #creating keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Помощь")
    item2 = types.KeyboardButton("Инструкция")
    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Давайте начнём! Используй команду \"Помощь\" для большей информации".
    format(message.from_user, bot.get_me()), parse_mode='html',
    reply_markup=markup)

@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text == 'Инструкция':
        bot.send_video(message.chat.id, 'BAACAgIAAxkBAAMMX7FX03zJauXhwXR1Hgt_V550TgcAAiELAAI2MIhJi8HoOTFnKUUeBA')
    elif message.text == 'Помощь':
        bot.send_message(message.chat.id, 'Для того, чтобы принять участие в конкурсе, просто отправьте мне Вашу работу как файл, если отправка происходит с телефона. Если Вы работаете с компьютера, отправляйте без сжатия. Работы принимаются с четверга по субботу включительно. Можете отправлять несколько работ, но зачтётся только последняя. Если у Вас возникли проблемы с отправкой работы, посмотрите \"Инструкция\". У Вашего профиля Telegram должно быть установлено имя пользователя, чтобы мы могли с Вами связаться')
    else:
        bot.send_video(message.chat.id, 'Извините, не понял Вас')



#downloading photos
@bot.message_handler(content_types=["document"])
def download(message):
    if message.from_user.username != None:
        if parseFromat(message.document.file_name) == 1:
            if (dayOfWeek() == 6 or dayOfWeek() == 4 or dayOfWeek() == 5): 
                chat_id = message.chat.id
                file_infos = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_infos.file_path)
                #Here is the path
                src = '/app/TelegramBotPy/media/' + message.from_user.username + '.jpg'
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.reply_to(message, "Спасибо за участие, фотограифия была добавлена")
            else:
                bot.send_message(message.chat.id, "Конкурс закончился. Ждём следующий")
        else:
            bot.send_message(message.chat.id, "Поддерживаются форматы только .jpg  и .png")
    else:
        bot.send_message(message.chat.id, "Похоже, что у Вас не установлено имя пользователя в Вашем профиле")

@bot.message_handler(content_types=["photo"])
def exception_photo(message):
    bot.send_message(message.chat.id, "Отправьте мне Вашу работу как файл, если отправка происходит с телефона. Если Вы работаете с компьютера, отправляйте без сжатия")

@bot.message_handler(content_types=["video"])
def exception_video(message):
    bot.send_message(message.chat.id, "В качестве работ принимаются только фотографии")

@bot.message_handler(content_types=["audio"])
def exception_audio(message):
    bot.send_message(message.chat.id, "В качестве работ принимаются только фотографии")

@bot.message_handler(content_types=["voice"])
def exception_voice(message):
    bot.send_message(message.chat.id, "К сожалению я не могу это послушать")

bot.polling(none_stop=True)

