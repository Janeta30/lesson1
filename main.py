import requests
import datetime #для преобразования времени рассвета и заката
from pprint import pprint
from config import open_weather_token

def get_weather(city, open_weather_token):

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
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
            )
        data = r.json()
        #pprint(data)

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

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f'Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n'
            f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м/с\n'
            f'Восход солнца: {sunrise_timestamp}\nЗакат: {sunset_timestamp}\nПродолжительность светового дня: {length_of_the_day}\n'
            f'Хорошего дня!'
            )
    except Exception as ex:
        print(ex)
        print('Проверьте название города')

def main():
    city = input('Введите город: ')
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    main()