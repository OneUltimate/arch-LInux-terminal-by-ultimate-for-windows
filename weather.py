import requests


city1 = ['Москва', 'Рязань', 'Уфа', 'Париж']

for city1 in city1:
    url1 = 'https://api.openweathermap.org/data/2.5/weather?q='+city1+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

def temp1():
    try:
        weather_data = requests.get(url1).json()
        temperature = round(weather_data['main']['temp'])
          
        temperature = str(temperature)
        if temperature[0] != '+':
            temperature = '+' + temperature 
        
            return temperature
    except:
        return 'N/A'

