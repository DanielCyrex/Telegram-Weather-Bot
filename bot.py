import telebot
import time
from telebot import types
from telebot.types import Message, CallbackQuery
import cityparser
import sys

TOKEN = 'Your token'
STICKER_ID = 'CAACAgIAAxkBAAMjXsG_ocvu1dbBNCYaT8Lm3l9IfRMAAl0AA0QNzxfHvudczhgCPBkE'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def command_handler(message: Message) -> None:
    Greeting = f"Привет <b>{message.from_user.first_name}</b>, " \
               f"я бот-синоптик по имени Льюис. " \
               "Я могу предоставить тебе прогноз погоды на сегодня, " \
               "тебе лишь стоит написать название города."

    if message.text == "/start":
        bot.send_sticker(message.chat.id, STICKER_ID)
        bot.send_message(message.chat.id, Greeting, parse_mode='html')
    elif message.text == "/help":
        Help = "Просто напиши название города на русском."
        bot.send_message(message.chat.id, Help, parse_mode='html')


@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def reply_to_message(message: Message) -> None:

    weather = cityparser.parse(message.text)
    if weather is None:
        send = "Прости, но я не знаю такого города 😢."
        bot.send_message(message.chat.id, send)
    else:
        TEMPERATURE = weather[0]['temp']
        DESCRIPTION = weather[0]['description']
        FEELS_LIKE = weather[0]['feels like']
        PRESSURE = weather[0]['pressure']
        HUMIDITY = weather[0]['humidity']
        WIND = weather[0]['wind']
        send = f'<u>Температура:</u> {TEMPERATURE}\n{DESCRIPTION}'
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Детальнее",
                                                     callback_data=f'{FEELS_LIKE},{WIND},{HUMIDITY},{PRESSURE}')
        keyboard.add(callback_button)
        bot.send_message(message.chat.id, send, parse_mode='html', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def detailed_weather(call: CallbackQuery) -> None:
    [FEELS_LIKE, WIND, HUMIDITY, PRESSURE] = (call.data).split(',')
    detailed_send = f'Чувствуется как: <b>{FEELS_LIKE}С</b>\n' \
                    f'Скорость ветра: <b>{WIND} м/c</b>\n' \
                    f'Влажность: <b>{HUMIDITY}%</b>\n' \
                    f'Давление: <b>{PRESSURE} мм</b>\n'
    bot.send_message(call.message.chat.id, detailed_send, parse_mode='html')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(e)
            time.sleep(15)
