from .terminal_plugin import Plugin
import requests
import os


class WeatherPlugin(Plugin):
    def __init__(self, terminal):
        super().__init__(terminal)  
        self.api_key = None  
        
    def setup(self):
        """Инициализация плагина"""
        self.api_key = '9d1ca96933b0328e1c7e3e7a26cb347'
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
        
    def get_weather(self, city):
        
            
            
        try:
            api_key = '9d1ca96933b0328e1c7e3e7a26cb347'
            url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('cod') != 200:
                error_msg = data.get('message', 'Неизвестная ошибка API')
                self.terminal.add_line(f"❌ Ошибка: {error_msg}", 'highlight')
                return
                
            weather_info = (
                f"🌦️ Погода в {city}:\n"
                f"🌡️ Температура: {data['main']['temp']:.1f}°C\n"
                f"💧 Влажность: {data['main']['humidity']}%\n"
                f"🌀 Давление: {data['main']['pressure']} hPa\n"
                f"🌬️ Ветер: {data['wind']['speed']} м/с"
            )
            self.terminal.add_line(weather_info or 'neCon ', 'normal')
            
        except requests.exceptions.RequestException as e:
            self.terminal.add_line(f"❌ Ошибка соединения: {str(e)}", 'highlight')
        except Exception as e:
            self.terminal.add_line(f"❌ Неожиданная ошибка: {str(e)}", 'highlight')
        finally:
            self.terminal.show_prompt()