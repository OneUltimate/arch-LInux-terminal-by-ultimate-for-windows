from .terminal_plugin import Plugin
import webbrowser
from urllib.parse import quote

class SearchPlugin(Plugin):
    def __init__(self, terminal):
        super().__init__(terminal)
        self.register_command("google", "Поиск в Google", self.handle_google)
        self.register_command("search", "Универсальный поиск", self.handle_search)
    
    def handle_google(self, command):
        
        if len(command.split()) < 2:
            self.terminal.add_line("Использование: google <запрос>", 'highlight')
            return
            
        query = quote(' '.join(command.split()[1:]))
        webbrowser.open(f"https://www.google.com/search?q={query}")
        self.terminal.add_line(f"🔍 Открываю Google с запросом: {query}", 'normal')
    
    def handle_search(self, command):
    
        parts = command.split()
        if len(parts) < 3:
            self.terminal.add_line(
                "Использование: search <сервис> <запрос>\n"
                "Доступные сервисы: google, youtube, github, stackoverflow", 
                'highlight'
            )
            return
            
        service = parts[1].lower()
        query = quote(' '.join(parts[2:]))
        
        urls = {
            'google': f'https://google.com/search?q={query}',
            'youtube': f'https://youtube.com/results?search_query={query}',
            'github': f'https://github.com/search?q={query}',
            'stackoverflow': f'https://stackoverflow.com/search?q={query}'
        }
        
        if service in urls:
            webbrowser.open(urls[service])
            self.terminal.add_line(f"🌐 Поиск на {service}: {query}", 'normal')
        else:
            self.terminal.add_line(f"❌ Неизвестный сервис: {service}", 'highlight')
    
    def get_help(self):
        return (
            "🔍 Поисковые команды:\n"
            "  google <запрос>   - Поиск в Google\n"
            "  search <сервис> <запрос> - Поиск на разных платформах\n"
            "  Доступные сервисы: google, youtube, github, stackoverflow\n"
            "  Примеры:\n"
            "  google python tutorial\n"
        )