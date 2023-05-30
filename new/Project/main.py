import telebot
from telebot import types
from config import *
from main_func import get_information
from translate_func import get_translate
from texts import *
import sqlite3

API_TOKEN = TOKEN

bot = telebot.TeleBot(API_TOKEN)

dct_user = {
    'free_spin': True,  # Один бесплатный прогноз
    'city': '',  # Введенный город
    'write_city': False,  # Ожидание ввода города пользователем
    'write_name': False,  # Ожидание ввода имени пользователем
    'name': '',  # Введенный имя
}


@bot.message_handler(commands=['start'])  # Декоратор, который реагирует на команду start
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создаем сетку для главных кнопочек
    item1 = types.KeyboardButton(
        'Получить бесплатный прозноз погоды на сегодня')  # Создаем кнопочку
    item2 = types.KeyboardButton('Вопрос/Ответ')  # Создаем кнопочку
    item3 = types.KeyboardButton('Регистрация')  # Создаем кнопочку
    markup.add(item1)
    markup.add(item2, item3)
    mes = MESSAGE_START.format(name_user=message.from_user.first_name)
    bot.send_message(message.chat.id, mes, reply_markup=markup)

@bot.message_handler(commands=['help'])  # Декоратор, который реагирует на команду help
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создаем сетку для главных кнопочек
    item1 = types.KeyboardButton(
        'Начать использовать')  # Создаем кнопочку
    item2 = types.KeyboardButton('Вопрос/Ответ')  # Создаем кнопочку
    markup.add(item1)
    markup.add(item2)
    mes = MESSAGE_HELP
    bot.send_message(message.chat.id, mes, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def run(message):
    user_message = message.text  # Получаем значение, которое отправил пользователь
    if user_message == 'Получить бесплатный прозноз погоды на сегодня':
        if dct_user['free_spin']:  # !!!! ЕСЛИ ПОЛЬЗОВАТЕЛЬ НОВЫЙ
            bot.send_message(message.chat.id, 'Напиши свой город')
            dct_user['write_city'] = True
    elif user_message == 'Вопрос/Ответ':
        question_answer(message)
    elif user_message == 'Регистрация':
        bot.send_message(message.chat.id, 'Введи свое имя')
        dct_user['write_name'] = True
    elif user_message == 'Начать использовать':
        start(message)
    else:
        if dct_user['write_city']:
            dct_user['write_city'] = False
            dct_user['city'] = user_message
            get_forecast_today(message)
        elif dct_user['write_name']:
            dct_user['write_name'] = False
            dct_user['name'] = user_message
            put_to_database(message)
        else:
            bot.send_message(message.chat.id, 'Иди нафиг, я от тебя ничего не жду')

def get_forecast_today(message):
    try:
        dct_information = get_information(dct_user.get('city'))
        type_of_weather = dct_information.get('type_of_weather', 'Error')
        today_day = dct_information.get('today_day', 'Error')
        altimetr = dct_information.get('altimetr', 'Error')
        snow_detect = dct_information.get('snow_detect', 'Error')
        sun_rise = dct_information.get('sun_rise', 'Error')
        sun_set = dct_information.get('sun_set', 'Error')
        temperature = dct_information.get('temperature', 'Error')
        temperature_feel = dct_information.get('temperature_feel', 'Error')
        temperature_max = dct_information.get('temperature_max', 'Error')
        temperature_min = dct_information.get('temperature_min', 'Error')
        wind_speed = dct_information.get('wind_speed', 'Error')

        today_day = get_translate(today_day)
        type_of_weather = get_translate(type_of_weather)

        RESULT = TODAY_WEATHER.format(
            type_of_weather=type_of_weather,
            today_day=today_day,
            altimetr=altimetr,
            snow_detect=snow_detect,
            sun_rise=sun_rise,
            sun_set=sun_set,
            temperature=temperature,
            temperature_feel=temperature_feel,
            temperature_max=temperature_max,
            temperature_min=temperature_min,
            wind_speed=wind_speed)

        bot.send_message(message.chat.id, RESULT)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка, попробуй еще раз')
        dct_user['write_city'] = True

def put_to_database(message):
    try:
        connect = sqlite3.connect('data/database.db')
        cursor = connect.cursor()

        name = dct_user.get('name')
        id_user = message.from_user.id

        sql = f'''
        SELECT * FROM users
        WHERE users_id = {id_user}
        '''
        result = cursor.execute(sql).fetchone()
        if not result:

            sql = f'''
            INSERT INTO users(users_id, users_name)
            VALUES({id_user}, "{name}")
            '''
            cursor.execute(sql)
            connect.commit()
            connect.close()
            bot.send_message(message.chat.id, 'Успешно')
        else:
            bot.send_message(message.chat.id, 'Вы уже зареганы')
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка')

def question_answer(message):
    bot.send_message(message.chat.id, 'question_answer')



if __name__ == '__main__':
    print(START_MESSAGE)
    bot.polling(none_stop=True)
