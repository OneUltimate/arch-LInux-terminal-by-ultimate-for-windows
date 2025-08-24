from .terminal_plugin import Plugin
import psutil

class NetstatPlugin(Plugin):
    
    def __init__(self, terminal):
        super().__init__(terminal)
        self.register_command("ns", "Список соедеденений", self.handle_netstat)
           

    def handle_netstat(self, command):
        try:
            conns = psutil.net_connections()
            for conn in conns[:20]:
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                self.terminal.add_line(f"{laddr} -> {raddr} {conn.status}", 'normal')
        except Exception as e:
            self.terminal.add_line(f"Ошибка: {e}", 'highlight')
        finally:
            self.terminal.show_prompt()
    
    def get_help(self):
        return (
        "ns - Список активных сетевых соединений\n"
        "Показывает первые 20 соединений с адресами и статусами\n"
        "Формат вывода: [локальный_адрес] -> [удаленный_адрес] [статус]"
        )