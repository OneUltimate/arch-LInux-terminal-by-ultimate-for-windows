import requests
from dotenv import load_dotenv 

CITY = os.getenv("CITY")

city = CITY or ['Москва', 'Рязань', 'Уфа', 'Париж']

for city in city:
    url1 = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

def temp1():
    try:
        weather_data = requests.get(url1).json()
        temperature = round(weather_data['main']['temp'])
          
        temperature = str(temperature)
        if temperature[0] != '+':
            temperature = '+' + temperature 
        
            return temperature
        else:
            return temperature
    except:
        return 'N/A'


