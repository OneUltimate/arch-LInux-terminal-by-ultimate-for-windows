from .terminal_plugin import Plugin
import psutil
import platform
import os 

class ProcessPlugin(Plugin):
    def __init__(self, terminal):
        super().__init__(terminal)
        self.register_command("ps", "Список процессов", self.handle_ps)
        self.register_command("kill", "Завершить процесс", self.handle_kill)
        
    def setup(self):
        pass

    def handle_ps(self, command: str):
        
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    processes.append(proc.info)
                except psutil.NoSuchProcess:
                    continue
            
           
            processes.sort(key=lambda p: p['name'].lower())
            
            self.terminal.add_line("🔄 Список процессов (PID - Имя - Пользователь):", 'highlight')
            for p in processes[:20]:
                self.terminal.add_line(f"{p['pid']} - {p['name']} - {p['username']}", 'normal')
            
            self.terminal.add_line(f"\nВсего процессов: {len(processes)}", 'highlight')
            
        except Exception as e:
            self.terminal.add_line(f"❌ Ошибка: {str(e)}", 'highlight')
        finally:
            self.terminal.show_prompt()

    def handle_kill(self, command: str):
        parts = command.split()
        if len(parts) < 2:
            self.terminal.add_line("Использование: kill <PID или имя>", 'highlight')
            return
            
        target = parts[1]
        try:
            if target.isdigit():  # Если ввели PID
                pid = int(target)
                if platform.system() == "Windows":
                    os.system(f"taskkill /pid {pid} /f")
                else:
                    os.kill(pid, 9)
            else:  # Если ввели имя процесса
                if platform.system() == "Windows":
                    os.system(f"taskkill /im {target} /f")
                else:
                    os.system(f"pkill {target}")
                    
            self.terminal.add_line(f"✅ Процесс {target} завершен", 'normal')
        except Exception as e:
            self.terminal.add_line(f"❌ Ошибка: {str(e)}", 'highlight')



    def get_help(self):
        return (
            "ps - показать список процессов\n"
            "kill <PID> - завершить процесс"
        )