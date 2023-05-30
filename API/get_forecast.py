import requests


def forecast(date, latitude, longtitude):
	url_2 = 'https://weather338.p.rapidapi.com/weather/forecast'

	params = {
		"date": date,
		"latitude": latitude,
		"longitude": longtitude,
		"language": 'en-US',
		"units": 'm'
	}

	headers = {  # TOKEN, вспомогательный переменные
		'X-RapidAPI-Key': 'ea39ae6397mshabef898eb8888c1p1e8bc7jsn691e14c8b25c',
		'X-RapidAPI-Host': 'weather338.p.rapidapi.com'
	}

	response = requests.get(url_2, headers=headers, params=params).json()
	return response









