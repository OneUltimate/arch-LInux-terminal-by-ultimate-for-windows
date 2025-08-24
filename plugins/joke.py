from .terminal_plugin import Plugin
import requests

class JokePlugin(Plugin):
    
    def __init__(self, terminal):
        super().__init__(terminal)
        self.register_command("joke", "рандомный анекдот", self.handle_joke)
        
    def handle_joke(self, command):
    
        joke = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        self.terminal.add_line(f"{joke['setup']}\n{joke['punchline']}", 'normal')