from telebot import TeleBot
from telebot import apihelper

import config
from models import models
from models import exceptions


apihelper.proxy = config.PROXY
bot = TeleBot(config.TELEGRAM_TOKEN)


# Handling start

@bot.message_handler(commands=['start'])
def handle_start(message):
    text = 'Добро пожаловать! Необходимо пройти регистрацию. Нажмите сюда /registration'
    bot.send_message(chat_id=message.chat.id, text=text)


# Handling registration

@bot.message_handler(commands=['registration'])
def handle_registration(message):
    customer = models.Customer(id=message.chat.id)
    text = 'Введите, пожалуйста Ваше имя:'
    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message, handle_first_name, customer)


def handle_first_name(message, customer):
    try:
        customer.first_name = message.text
    except TypeError as e:
        text = str(e)
    except exceptions.FieldIsTooLong as e:
        text = str(e)
    except exceptions.FieldNotMatchPattern as e:
        text = str(e)
    else:
        text = 'Введите, пожалуйста Вашу фамилию:'
        bot.send_message(chat_id=message.chat.id, text=text)
        bot.register_next_step_handler(message, handle_last_name, customer)

        return

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message, handle_first_name, customer)


def handle_last_name(message, customer):
    try:
        customer.last_name = message.text
    except TypeError as e:
        text = str(e)
    except exceptions.FieldIsTooLong as e:
        text = str(e)
    except exceptions.FieldNotMatchPattern as e:
        text = str(e)
    else:
        text = 'Введите, пожалуйста Ваш телефон:'
        bot.send_message(chat_id=message.chat.id, text=text)
        bot.register_next_step_handler(message, handle_phone, customer)

        return

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message, handle_last_name, customer)


def handle_phone(message, customer):
    try:
        customer.phone = message.text
    except TypeError as e:
        text = str(e)
    except exceptions.FieldIsTooLong as e:
        text = str(e)
    except exceptions.FieldNotMatchPattern as e:
        text = str(e)
    else:
        text = 'Введите, пожалуйста Вашу электронную почту:'
        bot.send_message(chat_id=message.chat.id, text=text)
        bot.register_next_step_handler(message, handle_email, customer)

        return

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message, handle_phone, customer)


def handle_email(message, customer):
    try:
        customer.email = message.text
    except TypeError as e:
        text = str(e)
    except exceptions.FieldIsTooLong as e:
        text = str(e)
    except exceptions.FieldNotMatchPattern as e:
        text = str(e)
    else:
        customer.create()
        text = 'Данные успешно сохранены.'
        bot.send_message(chat_id=message.chat.id, text=text)

        return

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message, handle_email, customer)
