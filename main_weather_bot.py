import requests
import datetime #для преобразования времени рассвета и заката
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши мне название города и я пришлю сводку погоды')

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облочно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzele': 'Дождь \U00002614', 
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }#Эмодзи погоды

    try:
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
            )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']# текущая погода

        weather_description = data['weather'][0]['main'] #состояние погоды
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, не пойму что там за погода!'

        humidity = data['main']['temp']# влажность
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f'Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n'
            f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м/с\n'
            f'Восход солнца: {sunrise_timestamp}\nЗакат: {sunset_timestamp}\nПродолжительность светового дня: {length_of_the_day}\n'
            f'---Хорошего дня!---'
            )
    except Exception as ex:
        await message.reply('\U00002620 Проверьте название города \U00002620')



if __name__ == '__main__':
    executor.start_polling(dp)