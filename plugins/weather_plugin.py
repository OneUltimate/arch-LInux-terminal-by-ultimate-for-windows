from .terminal_plugin import Plugin
import requests
import time

class WeatherPlugin(Plugin):
    def __init__(self, terminal):
        super().__init__(terminal)  
        self.api_key = None  
        
    def setup(self):
        self.api_key = '79d1ca96933b0328e1c7e3e7a26cb347'
        if not self.api_key:
            self.terminal.add_line("⚠️ Внимание: API ключ для погоды не задан", 'highlight')
        
    def handle_command(self, command: str) -> bool:
        if command.startswith('weather '):
            city = command[8:].strip()
            if city:
                self.get_weather(city)
            else:
                self.terminal.add_line("Использование: weather <город>", 'highlight')
            return True
        return False
        
    def get_weather_cached(self, city):
        cache_key = f"weather_{city}"
        
        if hasattr(self.terminal, 'cache'):
            cached = self.terminal.cache.get(cache_key, 600) 
            if cached is not None:
                return cached
        
        try:
            api_key = '79d1ca96933b0328e1c7e3e7a26cb347'
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={api_key}'

            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('cod') != 200:
                error_msg = data.get('message', 'Неизвестная ошибка API')
                return {'error': error_msg}
                
            weather_info = {
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind': data['wind']['speed'],
                'description': data['weather'][0]['description'] if data['weather'] else 'N/A'
            }

            if hasattr(self.terminal, 'cache'):
                self.terminal.cache.set(cache_key, weather_info)
                
            return weather_info
            
        except requests.exceptions.RequestException as e:
            return {'error': f"Ошибка соединения: {str(e)}"}
        except Exception as e:
            return {'error': f"Неожиданная ошибка: {str(e)}"}
        
    def get_weather(self, city):
        weather_data = self.get_weather_cached(city)
        
        if 'error' in weather_data:
            self.terminal.add_line(f"❌ {weather_data['error']}", 'highlight')
            return
            
        weather_info = (
            f"🌦️ Погода в {city}:\n"
            f"🌡️ Температура: {weather_data['temp']:.1f}°C\n"
            f"💧 Влажность: {weather_data['humidity']}%\n"
            f"🌀 Давление: {weather_data['pressure']} hPa\n"
            f"🌬️ Ветер: {weather_data['wind']} м/с\n"
            f"☁️  Описание: {weather_data['description']}\n"
        )
        self.terminal.add_line(weather_info, 'normal')
            
    def get_help(self):
        return "weather <город(ru/en)> - погода в городе в данный момент (кэшируется на 10 минут)"