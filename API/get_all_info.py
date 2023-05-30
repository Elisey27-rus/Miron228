from config import dict_form_eng_to_rus
from deep_translator import GoogleTranslator

def get_result(forecast, current_date, dict_form_eng_to_rus):
    forecast_for_today = forecast.get("v3-wx-observations-current", "Error")
    if forecast_for_today != "Error":
        result = {'current_date': current_date,
                  "dayOfWeek": forecast_for_today['dayOfWeek'],
                  "temperature": forecast_for_today['temperature'],
                  "temperatureFeelLike": forecast_for_today['temperatureFeelsLike'],
                  "temperatureMax24Hour": forecast_for_today['temperatureMax24Hour'],
                  "cloudCoverPhrase": forecast_for_today['cloudCoverPhrase'],
                  "pressureAltimeter": forecast_for_today['pressureAltimeter'],
                  }
    else:
        print('Город не найден.')
        result = False


    if result:
        day_of_week = result.get("dayOfWeek", "Error")
        temperature = result.get("temperature", "Error")
        temperature_feel_like = result.get('temperatureFeelLike', 'Error')
        temperature_max_24_hour = result.get("temperatureMax24Hour", "Error")
        cloud_cover_phrase = result.get("cloudCoverPhrase", "Error")
        pressure_altimeter = result.get("pressureAltimeter", "Error")

        if cloud_cover_phrase not in dict_form_eng_to_rus:
                translated = GoogleTranslator(source='auto', target='ru').translate(cloud_cover_phrase)
                dict_form_eng_to_rus[cloud_cover_phrase] = translated


        weather = "Дата: {current_date}\n" \
                   "День недели: {dayOfWeek}\n" \
                   "Температура на сегодня: {temperature}\n" \
                   "Ощущается как: {temperatureFeelLike}\n" \
                   "Лучшая температура за сегодня: {temperatureMax24Hour}\n" \
                   "Тип погоды на сегодня: {cloudCoverPhrase}\n" \
                   "Атмосферное давление: {pressureAltimeter}\n"


        dict_weather = weather.format(
                current_date=current_date,
                dayOfWeek=dict_form_eng_to_rus.get(day_of_week),
                temperature=temperature,
                temperatureFeelLike=temperature_feel_like,
                temperatureMax24Hour=temperature_max_24_hour,
                cloudCoverPhrase=dict_form_eng_to_rus.get(cloud_cover_phrase),
                pressureAltimeter=pressure_altimeter,
                )

        return dict_weather
    return "Error"