from .terminal_plugin import Plugin



class ShifrePlugin(Plugin):
    def __init__(self, terminal):
        super().__init__(terminal)
        self.register_command("shifre", "шифр цезаря", self.ss)
        pass
    def ss():
        pass