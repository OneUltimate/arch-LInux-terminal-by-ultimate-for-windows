import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))  

class Plugin:
    """Базовый класс для всех плагинов"""
    def __init__(self, terminal):
        self.terminal = terminal
        self.commands = {} 
    def setup(self):
        """Вызывается при загрузке плагина"""
        pass
        
    def register_command(self, command: str, description: str, handler):
        """Регистрирует новую команду"""
        self.commands[command] = (description, handler)
        
    def handle_command(self, command: str) -> bool:
        """Обрабатывает команду"""
        for cmd, (desc, handler) in self.commands.items():
            if command.startswith(cmd):
                handler(command)
                return True
        return False