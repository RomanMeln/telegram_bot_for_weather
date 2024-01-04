import telebot
import requests
import json
from telebot import types
from api_token import API

bot = telebot.TeleBot(API)
API = '372be3d68d7643299e3170944232312'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'<b>Бот показывает погоду</b>', parse_mode='html')
    markup = types.InlineKeyboardMarkup()
    # print(markup)
    markup.add(types.InlineKeyboardButton('Усинск', callback_data='usinsk'))
    bot.reply_to(message, 'Нажми кнопку или напиши название города', reply_markup=markup)


# декоратор который обрабатывает "callback_data='delete'", "callback_data='edit'" , короче callback_data=
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # print(callback)
    if callback.data == 'usinsk':
        res = requests.get(f'http://api.weatherapi.com/v1/current.json?key={API}&q=усинск&aqi=no')
        if res.status_code == 200:
            data = json.loads(res.text)
            # print(data)
            temp = data["current"]["temp_c"]
            wind_ms = round(data["current"]["wind_kph"] * 1000 / 3600, 2)
            feels_like_c = data["current"]["feelslike_c"]
            bot.send_message(callback.message.chat.id,
                         f'Погода сейчас: \nтемпература = {temp}, ветер = {wind_ms} м/с, ощущается как = {feels_like_c}')
        else:
            bot.send_message(callback, 'К сожалению, кнопка не работает')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower() # strip() удаляет пробелы до и после текста

    res = requests.get(f'http://api.weatherapi.com/v1/current.json?key={API}&q={city}&aqi=no')
    if res.status_code == 200:
        data = json.loads(res.text)
        # print(data)
        temp = data["current"]["temp_c"]
        wind_ms = round(data["current"]["wind_kph"] * 1000 / 3600, 2)
        feels_like_c = data["current"]["feelslike_c"]
        bot.reply_to(message, f'Погода сейчас: \n температура = {temp}, ветер = {wind_ms} м/с, ощущается как = {feels_like_c}')
    else:
        bot.reply_to(message, 'Город указан неверно')


# бесконечная работа бота
bot.polling(none_stop=True)

