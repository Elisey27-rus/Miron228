import requests
import sqlite3
from datetime import datetime as dt


def get_coords(query):
    url_coords = "https://weather338.p.rapidapi.com/locations/search"  # Ссылка для получения API ответа

    params = {  # Что хотим получить
        "query": query,
        "language": "ru_RU"
    }

    headers = {  # TOKEN, вспомогательный переменные
        "X-RapidAPI-Key": "6001830f9fmshedde88314ea83b2p16fc62jsna6ba91b12820",
        "X-RapidAPI-Host": "weather338.p.rapidapi.com"
    }

    response = requests.get(url_coords, headers=headers, params=params).json()

    # print(__import__('pprint').pprint(response))

    res = response.get('location', 'Error')
    if res != 'Error':
        latitude = res.get('latitude', 'Error')[0]
        longitude = res.get('longitude', 'Error')[0]

        # print(f"latitude: {latitude}, longitude: {longitude}")
        return (latitude, longitude)
    return 'Error'


def get_forecast(latitude, longitude, data=str(dt.now().date()).replace('-', '')):
    url_forecase = "https://weather338.p.rapidapi.com/weather/forecast"

    params = {
        "date": data,
        "latitude": latitude,
        "longitude": longitude,
        "language": "ru_RU",
        "units": "m"}

    headers = {
        "X-RapidAPI-Key": "6001830f9fmshedde88314ea83b2p16fc62jsna6ba91b12820",
        "X-RapidAPI-Host": "weather338.p.rapidapi.com"
    }

    response = requests.get(url_forecase, headers=headers, params=params).json()

    res = response.get('v3-wx-observations-current', 'Error')
    # print(__import__('pprint').pprint(res))
    if res != 'Error':
        dct_information = {
            'type_of_weather': res.get('cloudCoverPhrase', 'Error'),
            'today_day': res.get('dayOfWeek', 'Error'),
            'altimetr': res.get('pressureAltimeter', 'Error'),
            'snow_detect': res.get('snow24Hour', 'Error'),
            'sun_rise': res.get('sunriseTimeLocal', 'Error'),
            'sun_set': res.get('sunsetTimeLocal', 'Error'),
            'temperature': res.get('temperature', 'Error'),
            'temperature_feel': res.get('temperatureFeelsLike', 'Error'),
            'temperature_max': res.get('temperatureMax24Hour', 'Error'),
            'temperature_min': res.get('temperatureMin24Hour', 'Error'),
            'wind_speed': res.get('windSpeed', 'Error')
        }

        return dct_information
    return 'Error'
    # =============================================================================


def get_information(query):
    res = get_coords(query)
    if res != 'Error':
        latitude, longitude = res
        dct_information = get_forecast(latitude, longitude)
        if dct_information != 'Error':
            dct_information['sun_rise'] = dct_information['sun_rise'][11:19]
            dct_information['sun_set'] = dct_information['sun_set'][11:19]
            return dct_information
        return 'Error'
    return 'Error'


# =================================================================

def get_users_name_from_users_id(users_id):
    with sqlite3.connect('data/database.db') as connect:
        cursor = connect.cursor()

        sql = f"""
        SELECT users_name FROM users
        WHERE users_id = "{users_id}"
        """

        users_name = cursor.execute(sql).fetchone()[0]
        return users_name

def get_users_spin_from_users_id(users_id):
    with sqlite3.connect('data/database.db') as connect:
        cursor = connect.cursor()

        sql = f"""
        SELECT users_spin FROM users
        WHERE users_id = "{users_id}"
        """

        users_name = cursor.execute(sql).fetchone()[0]
        return users_name


def check_here_users_id(users_id):
    with sqlite3.connect('data/database.db') as connect:
        cursor = connect.cursor()

        sql = f"""
        SELECT users_id FROM users
        """

        ids = [id[0] for id in cursor.execute(sql).fetchall()]
        return users_id in ids


def put_to_db(users_id, users_name=None, registration=False):
    if registration:
        if get_users_name_from_users_id(users_id):
            return 'Ты уже зареган'
        with sqlite3.connect('data/database.db') as connect:
            cursor = connect.cursor()

            sql = f"""
            UPDATE users
            SET users_name = "{users_name}", users_spin = 1000
            WHERE users_id = "{users_id}"
            """

            cursor.execute(sql)
            connect.commit()
            return True



    else:
        if check_here_users_id(users_id):
            return True
        with sqlite3.connect('data/database.db') as connect:
            cursor = connect.cursor()

            sql = f"""
            INSERT INTO users(users_id)
            VALUES("{users_id}")
            """

            cursor.execute(sql)
            connect.commit()
            return True


def lose_one_spin(users_id):
    count_of_spin = get_users_spin_from_users_id(users_id)
    if count_of_spin > 0:
        with sqlite3.connect('data/database.db') as connect:
            cursor = connect.cursor()

            sql = f"""
            UPDATE users
            SET users_spin = "{count_of_spin - 1}"
            WHERE users_id = "{users_id}"
            """

            cursor.execute(sql)
            connect.commit()
            return True
    return 'Не хватает спинов'


print(lose_one_spin(12))