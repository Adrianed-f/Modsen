import requests


api_key = "fc4a3860aab3609f18b56f08365106c2"
url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": "Minsk",
    "appid": api_key
}


response = requests.get(url, params=params)
print(response.status_code, response.text)