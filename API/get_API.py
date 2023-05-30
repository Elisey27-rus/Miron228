def get_api(request):
	import requests

	url = 'https://weather338.p.rapidapi.com/locations/search'

	params = {
		'query': request,
		'language': 'en-US',
	}

	headers = {  # TOKEN, вспомогательный переменные
		'X-RapidAPI-Key': 'ea39ae6397mshabef898eb8888c1p1e8bc7jsn691e14c8b25c',
		'X-RapidAPI-Host': 'weather338.p.rapidapi.com'
	}

	result = requests.get(url, headers=headers, params=params).json()
	return result



