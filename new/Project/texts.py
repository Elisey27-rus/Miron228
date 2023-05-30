from colorama import Fore, Style

TODAY_WEATHER = "Погода на {today_day}\n" \
                "Тип погоды: {type_of_weather}\n" \
                "Температура: {temperature}\n" \
                "Ощущается как: {temperature_feel}\n" \
                "Минимальная температура: {temperature_min}\n" \
                "Максимальная температура: {temperature_max}\n" \
                "Давление: {altimetr}\n" \
                "Cнег: {snow_detect}\n" \
                "Скорость ветра: {wind_speed}\n" \
                "Восход солнца: {sun_rise}\n" \
                "Заход солнца: {sun_set}"

START_MESSAGE = Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Бот успешно запущен!" + Fore.RESET + Style.NORMAL + '\n'

MESSAGE_START = "Привет, {name_user}\n" \
                "Я бот, который могу узнать погоды в твоем городе\n"
MESSAGE_HELP = "Основная инфа...."

