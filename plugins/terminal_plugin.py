import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))  

class Plugin:
    def __init__(self, terminal):
        self.terminal = terminal
        self.commands = {} 
    def setup(self):        
        pass
        
    def register_command(self, command: str, description: str, handler):      
        self.commands[command] = (description, handler)
        
    def get_help(self) -> str:
       
        help_lines = []
        for cmd, (desc, _) in self.commands.items():
            help_lines.append(f"{cmd.ljust(15)} - {desc}")
        return "\n".join(help_lines)    
        
    def handle_command(self, command: str) -> bool:        
        for cmd, (desc, handler) in self.commands.items():
            if command.startswith(cmd):
                handler(command)
                return True
        return False