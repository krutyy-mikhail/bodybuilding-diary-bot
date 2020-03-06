from telebot import TeleBot
from telebot import apihelper

import config
import environment as env
from models import models
from models import exceptions
from bot.utils import get_data_from_food_report


apihelper.proxy = config.PROXY
bot = TeleBot(config.TELEGRAM_TOKEN)


# Handling start.

@bot.message_handler(commands=['start'])
def handle_start(message):
    text = 'Добро пожаловать! Необходимо пройти регистрацию. Нажмите сюда /registration'
    bot.send_message(chat_id=message.chat.id, text=text)


# Handling registration.

@bot.message_handler(commands=['registration'])
def handle_registration(message):
    user = env.user_service.get(message.chat.id)
    if not user:
        user = models.User(id=message.chat.id)
        text = 'Введите, пожалуйста Ваше имя:'
        bot.send_message(chat_id=message.chat.id, text=text)
        bot.register_next_step_handler(message, handle_first_name, user)
    else:
        text = 'Вы уже зарегистрированы.'
        bot.send_message(chat_id=message.chat.id, text=text)


def handle_first_name(message, user):
    try:
        user.first_name = message.text
    except TypeError as e:
        text = str(e)
    except exceptions.FieldIsTooLong as e:
        text = str(e)
    except exceptions.FieldNotMatchPattern as e:
        text = str(e)
    else:
        text = 'Введите, пожалуйста Вашу фамилию:'
        bot.send_message(chat_id=message.chat.id, text=text)
        bot.register_next_step_handler(message, handle_last_name, user)

        return

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message, handle_first_name, user)


def handle_last_name(message, user):
    try:
        user.last_name = message.text
    except TypeError as e:
        text = str(e)
    except exceptions.FieldIsTooLong as e:
        text = str(e)
    except exceptions.FieldNotMatchPattern as e:
        text = str(e)
    else:
        text = 'Введите, пожалуйста Ваш телефон:'
        bot.send_message(chat_id=message.chat.id, text=text)
        bot.register_next_step_handler(message, handle_phone, user)

        return

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message, handle_last_name, user)


def handle_phone(message, user):
    try:
        user.phone = message.text
    except TypeError as e:
        text = str(e)
    except exceptions.FieldIsTooLong as e:
        text = str(e)
    except exceptions.FieldNotMatchPattern as e:
        text = str(e)
    else:
        text = 'Введите, пожалуйста Вашу электронную почту:'
        bot.send_message(chat_id=message.chat.id, text=text)
        bot.register_next_step_handler(message, handle_email, user)

        return

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message, handle_phone, user)


def handle_email(message, user):
    try:
        user.email = message.text
    except TypeError as e:
        text = str(e)
    except exceptions.FieldIsTooLong as e:
        text = str(e)
    except exceptions.FieldNotMatchPattern as e:
        text = str(e)
    else:
        env.user_service.create(user)
        text = 'Данные успешно сохранены.'
        bot.send_message(chat_id=message.chat.id, text=text)

        return

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message, handle_email, user)
