
import sys

from PyQt5.QtWidgets import ( QApplication, QWidget, QTextEdit, QVBoxLayout, QLineEdit)
from PyQt5.QtCore import (QTimer, QDateTime, Qt, QProcess)
from PyQt5.QtGui import (QTextCursor, QTextCharFormat, QFont)

import platform
import os

import logging
from dotenv import load_dotenv
import importlib
import inspect
from pathlib import Path
import importlib.util
import time

from data.modules_plus.cheking_system import *
from data.modules_plus.proxy_checker import * 
from config import * 
from help_text import * 
from plugins.terminal_plugin import *
from data.help_databasa import help_database

from display_system_info import SystemInfoDisplay

load_dotenv()

logging.basicConfig(filename='terminal.log', level=logging.INFO)
            
class ArchTerminal(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(WINDOW_STYLE)
        self.setWindowTitle("ultimatum@arch")
        self.setGeometry(100, 100, 1000, 415)
        
        self.allowed_chat_id = ID_CHAT 
        self.colors = (ALL_COLORS)
        self.system_info_display = SystemInfoDisplay(self, self.colors)
        
        self.bg = BAGROUND_COLOR.get(
            os.getenv('baground_color', 'name'), 
            BAGROUND_COLOR['defoult']
        )
        
        self.font = QFont(SHRIFTE, 10)
        self.last_ip = ""
        self.last_network = ""
        self.command_history = []
        self.history_index = 0
        self.current_directory = os.getcwd()
        
        self.init_ui()
        
        self.system_info_display.display_system_info()
        self.system_info_display.setup_timers()
        
        self.show_prompt()
        
        self.plugins = [] 
        self.load_plugins() 
        
        self.telegram_bot = None  
        self.bot_token = BOT_TOKEN
        self.chat_id = None
        
        self.cache = CacheManager() 
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  
        self.setLayout(layout)
       

        terminal_container = QWidget()
        terminal_container.setStyleSheet(f"""
            background-color: rgba{self.bg['bg'].getRgb()};
            border-radius: 5px;
            border: 1px solid {self.colors['highlight'].name()};
        """)
        
        terminal_layout = QVBoxLayout(terminal_container)
        terminal_layout.setContentsMargins(5, 5, 5, 5)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(False)
        self.terminal.setFont(self.font)
        self.terminal.setStyleSheet(f"""
            QTextEdit {{
                background: transparent;
                color: {self.colors['normal'].name()};
                border: none;
                font-family: Consolas;
                font-size: 10pt;
            }}
        """)
        self.terminal.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.input_line = QLineEdit()
        self.input_line.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(50, 50, 50, 0.7);
                color: {self.colors['input'].name()};
                border: 1px solid {self.colors['highlight'].name()};
                font-family: Consolas;
                font-size: 10pt;
                border-radius: 3px;
                padding: 5px;
            }}
        """)
        self.input_line.returnPressed.connect(self.execute_command)
        
        terminal_layout.addWidget(self.terminal)
        terminal_layout.addWidget(self.input_line)
        layout.addWidget(terminal_container)
        
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.command_finished)

            
    def show_prompt(self):
       
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        format = QTextCharFormat()
        format.setForeground(self.colors['prompt'])
        cursor.setCharFormat(format)
        
        user = os.getenv('USERNAME') or os.getenv('USER') or 'user'
        host = platform.node()
        QTimer.singleShot(100, lambda: self.add_line(f"{user}@{host}:~{self.current_directory}$ ", 'prompt', auto_scroll=False))
                
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()
        
    def try_command(self, command):
        PW = os.getenv('POWERFUL_USER')
        PW = str(PW)
        if PW == '0':
            
            parts = command.split()
            if not parts:
                return False
        
            if parts[0] not in TRY_NOT_POWERFUL_USER_COMMAND: 
                TIME = QDateTime.currentDateTime().toString("HH:mm:ss")
                self.add_line(f"{TIME} - {command}", 'input')
                self.add_line("[!] command not ye", 'warning')
                return False
            else:
                return True
        else:
            return True
    
    def execute_command(self):
        command = self.input_line.text().strip()
        self.input_line.clear()
        
        if not command:
            self.show_prompt()
            return
        
        if self.try_command(command) == True:
                        
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            
            TIME = QDateTime.currentDateTime().toString("HH:mm:ss")
            self.add_line(f"{TIME} - {command}", 'input')
            
        
            handled = False
            for plugin in self.plugins:
                if plugin.handle_command(command):
                    handled = True
                    break
            
            
            if not handled:
                if command.lower() in ['exit', 'quit']:
                    QApplication.quit()
                elif command.startswith('cd '):
                    self.change_directory(command[3:].strip())
                elif command == 'clear':
                    self.terminal.clear()
                    self.show_prompt()
                elif command.startswith('!help'):
                    parts = command.split()
                    if len(parts) == 1:
                        self.show_help_1()
                    else:
                        try:
                            page = int(parts[1])
                            if page == 1:
                                self.show_help_1()
                            elif page == 2:
                                self.show_help_2()
                            elif page == 3:
                                self.show_help_3()
                            else:
                                self.add_line("Доступны страницы 1-3. Показана страница 1", "highlight")
                                self.show_help_1()
                        except ValueError:
                            self.add_line("Используйте: !help <1-3> (page) ", "highlight")
                            self.show_prompt()
                                                     
                    
                elif command == "startbot":
                    self.start_telegram_bot()
                elif command == 'stopbot':        
                    self.stop_bot()
                elif command == "restart":                                              
                    self.system_info_display.display_system_info() 
                elif command == "!help dsi":
                    self.add_line('display system information (DSI) - main function of the script', 'normal')
                    self.show_prompt()
                
                elif command == "reolad plugins":
                    self.plugins = []
                    self.load_plugins()
                    self.add_line("Плагины перезагружены", 'normal') 
                    
                    
                if command == 'plugin help':
                    def show_plugin_help():
                        
                        plugin_helps = []
                        for plugin in self.plugins:
                            if hasattr(plugin, 'get_help'):
                                help_text = plugin.get_help()
                                if help_text:
                                    plugin_helps.append(help_text)
                        
                        
                        if plugin_helps:
                            self.add_line("=== Доступные плагины ===", 'highlight')
                            for i, help_text in enumerate(plugin_helps, 1):
                                self.add_line(f"\n🔹 Плагин {i}:", 'normal')
                                self.add_line(help_text, 'normal')
                        else:
                            self.add_line("Нет доступных плагинов", 'highlight')
                    
                    show_plugin_help()
                    
                
                if command.startswith("data help "):
                    parts = command.split()
                                      
                    if len(parts) == 3:
                        self.data_help(parts[2])
                                                
                if command == ("data help"):
                    self.add_line("Доступные разделы справки:", 'highlight')
                    for key in help_database.keys():
                        self.add_line(f"  {key}", 'normal')
                    
                
                if command.startswith('welcome window '):
                    welcome_w = command.split()
                      
                    self.welcome_window_functoin(welcome_w[2])
                    return    
                
                if command.startswith('powerful '):
                    powerful_u = command[9:]
                    self.powerful_user_functoin(powerful_u)
                    return
                
                if command == 'env read':
                    self.show_env_command()
                    return
                
                elif command == 'cashe clear':
                    self.cache.clear()
                    self.add_line("✅ Кэш очищен", 'normal')
                    
                elif command == 'cashe stats':
                    stats = f"Кол-во записей: {len(self.cache.cache)} записей\n"
                    for key, value in self.cache.cache.items():
                        age = time.time() - self.cache.cache_times[key]
                        stats += f"{key}: {age:.1f} сек назад\n"
                    self.add_line(stats, 'normal')
                
                else:
                    self.process = QProcess(self)  
                    self.process.readyReadStandardOutput.connect(self.handle_stdout)
                    self.process.readyReadStandardError.connect(self.handle_stderr)
                    self.process.finished.connect(self.command_finished)
                    self.process.start(command)
        
                    
                logging.info(f' {TIME} - {command}')
    
    
    def show_env_command(self):
        
        try:
            env_path = '.env'
            
            with open(env_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                
            if not content:
                self.add_line("📝 Файл .env пуст", 'normal')
                return
                
            self.add_line("📁 Содержимое .env файла:", 'highlight')
            self.add_line("-" * 50, 'normal')
            
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                if not line:
                    continue
                    
                if line.startswith('#'):
                    self.add_line(line, 'comment')
                    continue
                    
                if '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip().replace('\n', ' ').replace('\r', ' ')
                    self.add_line(f"🔑 {key.strip()} = {value}", 'normal')
                else:
                    self.add_line(line, 'normal')
                    
        except FileNotFoundError:
            self.add_line("❌ Файл .env не найден", 'error')
        except Exception as e:
            self.add_line(f"❌ Ошибка чтения файла: {str(e)}", 'error')
    
    def welcome_window_functoin(self, new_value):

        if new_value not in ['0', '1']:
            self.add_line(fr'[error] "{new_value}" - неккоректное значение функции', 'error')
            return
        
        env_file = '.env'
        try: 
            with open(env_file, 'r') as f:
                lines = f.readlines()
            
            
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('WELCOME_WINDOW='):
                    lines[i] = f'WELCOME_WINDOW={new_value}\n'
                    updated = True
                    break
            
            with open(env_file, 'w') as f:
                f.writelines(lines)
                
            if new_value == '1':
                new_value = new_value + ' - True'
                
            if new_value == '0':
                new_value = new_value + ' - False'
            
            self.add_line(f"изменение значения welcome_window на {new_value}", 'highlight')
            
        except Exception as e:
            self.add_line(f"[error] Ошибка функции: {str(e)}", 'error')
                     
    def powerful_user_functoin(self, new_value):
            if new_value not in ['0', '1']:
                self.add_line(fr'[error] "{new_value}" - неккоректное значение функции', 'error')
                return
            env_file = '.env'
            try:
                with open(env_file, 'r') as f:
                    lines = f.readlines()
                updated = False
                for i, line in enumerate(lines):
                    if line.startswith('POWERFUL_USER='):
                        lines[i] = f'POWERFUL_USER={new_value}\n'
                        updated = True
                        break             
                with open(env_file, 'w') as f:
                    f.writelines(lines)
                if new_value == '1':
                    new_value = new_value + ' - True'
                if new_value == '0':
                    new_value = new_value + ' - False'
                self.add_line(f"изменение значения powerful_user на {new_value} \n <> Перезапустите терминал", 'highlight')

            except Exception as e:
                self.add_line(f"[error] Ошибка функции: {str(e)}", 'error')
    
    def load_plugins(self):        
        plugins_dir = Path(__file__).parent / "plugins"           
        plugins_dir.mkdir(exist_ok=True)
        
        QTimer.singleShot(10000, lambda: self.add_line(f"🔍 Поиск плагинов в: {plugins_dir}", 'normal', auto_scroll=False))
        
        print(f"[DEBUG] Plugins dir: {plugins_dir}")

        loaded_count = 0
        error_count = 0
        
        for plugin_file in plugins_dir.glob("*.py"):
            if plugin_file.stem in ["__init__", "terminal_plugin"]:
                continue
                
            plugin_name = plugin_file.stem
            module_name = f"plugins.{plugin_name}"
            
            try:     
                spec = importlib.util.spec_from_file_location(module_name, plugin_file)
                if spec is None:
                    raise ImportError(f"Не удалось создать spec для {plugin_name}")
                    
                module = importlib.util.module_from_spec(spec)
                
                sys.modules[module_name] = module  
                spec.loader.exec_module(module)
                
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, Plugin) and 
                        obj != Plugin):        
                        try:
                            plugin = obj(self)
                            plugin.setup()
                            self.plugins.append(plugin)
                            loaded_count += 1
                            msg = f"✅ Успешно загружен: {plugin_name}"
                            print(f"[SUCCESS] {msg}")
                            
                        except Exception as e:
                            error_count += 1
                            msg = f"⚠️ Ошибка инициализации {plugin_name}: {str(e)}"
                            print(f"[ERROR] {msg}")
                            import traceback
                            traceback.print_exc()
                            
            except Exception as e:
                error_count += 1
                msg = f"❌ Ошибка загрузки {plugin_name}: {str(e)}"
                print(f"[CRITICAL] {msg}")
                import traceback
                traceback.print_exc()
   
        summary = f"📊 Загружено плагинов: {loaded_count}"
        if error_count > 0:
            summary += f", ошибок: {error_count}"
        QTimer.singleShot(12000, lambda: self.add_line(summary, 'normal'))

        if loaded_count == 0:
            self.add_line('', 'normal')

    def change_directory(self, path):
        try:
            if not path:
                path = os.path.expanduser('~')
                
            new_path = os.path.abspath(os.path.join(self.current_directory, path))
            if os.path.isdir(new_path):
                self.current_directory = new_path
                self.add_line(f"Changed directory to: {self.current_directory}", 'normal')
            else:
                self.add_line(f"Directory not found: {new_path}", 'highlight')
        except Exception as e:
            self.add_line(f"Error changing directory: {str(e)}", 'highlight')
            
        self.show_prompt()
        
    def show_help_1(self):
        help_text = HELP_TEXT_1
        self.add_line(help_text, 'normal')
        self.show_prompt()
        
    def show_help_2(self):
        help_text = HELP_TEXT_2
        self.add_line(help_text, 'normal')
        self.show_prompt()   
    
    def show_help_3(self):    
        help_text = HELP_TEXT_3
        self.add_line(help_text, 'normal')
        self.show_prompt()
        
    def data_help(self, index):
        lower = index.lower()
        dh = help_database.get(lower)
        if dh:
            self.add_line(f'\n====={index.upper()}{12 * '='}', 'attention')
            self.add_line(f'Описание: {dh.get('description', '-----')}', 'normal')
            self.add_line(f'Синтаксис: {dh.get('syntax', 'Нет синтаксиса')}', 'normal')

            # self.add_line(dh.get('examples'), 'normal')
            
        else:
            self.add_line(f"❌ Раздел справки '{index}' не найден.", 'error')
            self.add_line("Используйте 'datahelp list' для просмотра доступных разделов.", 'normal')
        
    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        output = self.safe_decode_windows(data) if platform.system() == "Windows" else self.safe_decode(data)
        self.add_line(output, 'normal')

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        error = self.safe_decode_windows(data) if platform.system() == "Windows" else self.safe_decode(data)
        self.add_line(error, 'highlight')

    def safe_decode_windows(self, byte_data):
        try:
            import ctypes
            codepage = ctypes.windll.kernel32.GetConsoleOutputCP()
            return bytes(byte_data).decode(f'cp{codepage}')
        except:
            encodings = ['cp866', 'cp1251', 'utf-8']
            for encoding in encodings:
                try:
                    return bytes(byte_data).decode(encoding)
                except UnicodeDecodeError:
                    continue
        return bytes(byte_data).decode('utf-8', errors='replace')

    def safe_decode(self, byte_data):
        encodings = ['utf-8', 'latin-1', 'iso-8859-1']
        for encoding in encodings:
            try:
                return bytes(byte_data).decode(encoding)
            except UnicodeDecodeError:
                continue
        return bytes(byte_data).decode('utf-8', errors='replace')
        
    def command_finished(self):
        self.process.readyReadStandardOutput.disconnect()
        self.process.readyReadStandardError.disconnect()
        self.process.finished.disconnect()
        self.show_prompt()
        
    def add_line(self, text, color=None, auto_scroll=True):
        scrollbar = self.terminal.verticalScrollBar()
        old_scroll_pos = scrollbar.value()
        
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if color:
            format = QTextCharFormat()
            format.setForeground(self.colors[color])
            cursor.setCharFormat(format)
        
        cursor.insertText(text + "\n")
        
        if not auto_scroll:
            scrollbar.setValue(old_scroll_pos)
        else:
            scrollbar.setValue(scrollbar.maximum())
               
    def update_line(self, prefix, new_value, color=None):
        cursor = self.terminal.textCursor()
        scrollbar = self.terminal.verticalScrollBar()
        old_scroll_pos = scrollbar.value()
        
        full_text = self.terminal.toPlainText()
        
        pos = full_text.rfind(prefix)
        
        if pos == -1:
    
            self.add_line(f"                                      |{prefix}{new_value}", 
                        color or 'normal', 
                        auto_scroll=False)
        else:
           
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.StartOfLine)
            
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            
            cursor.removeSelectedText()
            
            format = QTextCharFormat()
            format.setForeground(self.colors[color] if color else self.colors['normal'])
            cursor.setCharFormat(format)
            
            cursor.insertText(f"                                      |{prefix}{new_value}\n")
        
        scrollbar.setValue(old_scroll_pos)    
   
   
   
class CacheManager:
    def __init__(self):
        self.cache = {}
        self.cache_times = {}
        
    def get(self, key, max_age=300):
        if key in self.cache and time.time() - self.cache_times[key] < max_age:
            return self.cache[key]
        return None
        
    def set(self, key, value):
        self.cache[key] = value
        self.cache_times[key] = time.time()
        
    def clear(self, key=None):
        if key:
            if key in self.cache:
                del self.cache[key]
                del self.cache_times[key]
        else:
            self.cache.clear()
            self.cache_times.clear()