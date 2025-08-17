



import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit, QVBoxLayout, 
                            QScrollBar, QLabel, QMainWindow, QPushButton, 
                            QHBoxLayout, QLineEdit)
from PyQt5.QtCore import QTimer, QDateTime, Qt, QProcess, QPropertyAnimation
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont, QFontDatabase
import platform
import psutil
import datetime
import time
import subprocess
import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import threading
import logging
from dotenv import load_dotenv
import importlib
import inspect
from pathlib import Path
import importlib.util

import getpass

from modules_plus.weather import *
from modules_plus.pc_information import *
from modules_plus.cheking_system import *
from modules_plus.proxy_checker import * 
from modules_plus.config import * 
from help_text import * 
from plugins.terminal_plugin import *

PC = []

load_dotenv()


logging.basicConfig(filename='terminal.log', level=logging.INFO)


class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setGeometry(0, 0, 1000, 415)
        self.setFixedSize(1000, 415)
        
        self.colors = {
            'bg': QColor(30, 30, 30, 230),  
            'text': QColor("#54EBFF"),
            'highlight': QColor('#34E2E2'),  
        }
        
        
        self.setStyleSheet(f"""
            background-color: rgba{self.colors['bg'].getRgb()};
            border-radius: 8px;
            border: 1px solid {self.colors['highlight'].name()};
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        font_id = QFontDatabase.addApplicationFont("VT323-Regular.ttf")  
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text'].name()};
                font-family: {font_family};
                font-size: 60px;
                
            }}
        """)
        self.layout.addWidget(self.label)
        
       
        self.username = os.getenv('USERNAME') or os.getenv('USER') or 'user'
        self.text_to_type = f"welcome mr.{self.username} "
        self.current_text = ""
        self.char_index = 0
        
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.type_next_char)
        self.timer.start(250) 
        
    def type_next_char(self):
        if self.char_index < len(self.text_to_type):
            self.current_text += self.text_to_type[self.char_index]
            self.label.setText(self.current_text)
            self.char_index += 1
        else:
            self.timer.stop()
            
            QTimer.singleShot(1200, self.close_splash)
            
    def close_splash(self):
        
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(self.close)
        self.animation.start()
        
        
        if self.parent:
            self.parent.show()


class ArchTerminal(QWidget):
    def __init__(self):
        super().__init__()
        
       
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(WINDOW_STYLE)
        self.setWindowTitle("ultimatum@arch")
        self.setGeometry(100, 100, 1000, 415)
        
        self.allowed_chat_id = ID_CHAT
        
        self.colors = (ALL_COLORS)
        
        self.font = QFont("Consolas", 10)
        self.last_ip = ""
        self.last_network = ""
        self.command_history = []
        self.history_index = 0
        self.current_directory = os.getcwd()
        
        self.init_ui()
        
        self.display_system_info()
        self.setup_timers()
        self.show_prompt()
        
        self.plugins = [] 
        self.load_plugins() 
        
        self.telegram_bot = None  
        self.bot_token = BOT_TOKEN
        self.chat_id = None
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  
        self.setLayout(layout)
       

        terminal_container = QWidget()
        terminal_container.setStyleSheet(f"""
            background-color: rgba{self.colors['bg'].getRgb()};
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
        cursor.insertText(f"{user}@{host}:~{self.current_directory}$ ")
        
        
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()
        
    def execute_command(self):
        command = self.input_line.text().strip()
        self.input_line.clear()
        
        if not command:
            self.show_prompt()
            return
            
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
                self.display_system_info()
            elif command == "!help dsi":
                self.add_line('display system information (DSI) - main function of the script', 'normal')
                self.show_prompt()
            
            elif command == "rp":
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
                    
            else:
                self.process = QProcess(self)  
                self.process.readyReadStandardOutput.connect(self.handle_stdout)
                self.process.readyReadStandardError.connect(self.handle_stderr)
                self.process.finished.connect(self.command_finished)
                self.process.start(command)
      
                
            logging.info(f' {TIME} - {command}')

    
    def load_plugins(self):
        
        plugins_dir = Path(__file__).parent / "plugins"
        
        
        plugins_dir.mkdir(exist_ok=True)
        
  
        self.add_line(f"🔍 Поиск плагинов в: {plugins_dir}", 'normal')
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
                            
                           
                            # self.add_line(msg, 'normal')
                            
                            print(f"[SUCCESS] {msg}")
                            
                        except Exception as e:
                            error_count += 1
                            msg = f"⚠️ Ошибка инициализации {plugin_name}: {str(e)}"
                            
                            # self.add_line(msg, 'highlight')
                            
                            print(f"[ERROR] {msg}")
                            import traceback
                            traceback.print_exc()
                            
            except Exception as e:
                error_count += 1
                msg = f"❌ Ошибка загрузки {plugin_name}: {str(e)}"
                
                # self.add_line(msg, 'highlight')
                
                print(f"[CRITICAL] {msg}")
                import traceback
                traceback.print_exc()
   
   
        summary = f"📊 Загружено плагинов: {loaded_count}"
        if error_count > 0:
            summary += f", ошибок: {error_count}"
        self.add_line(summary, 'normal')
        
        
        if loaded_count == 0:
            self.add_line('', 'normal')
    
    def start_telegram_bot(self):
            
            
            # if self.telegram_bot:
            #     self.add_line("Бот уже запущен!", 'highlight')
            #     return
            
            if not self.bot_token:
                self.add_line("Ошибка: Токен бота не найден в .env файле!", 'highlight')
                return
                
            if not self.allowed_chat_id:
                self.add_line("Ошибка: ALLOWED_CHAT_ID не задан в .env файле!", 'highlight')
                return

            self.add_line("Запускаю Telegram бота...", 'normal')

            def bot_thread():
                try:
                    updater = Updater(self.bot_token)
                    dispatcher = updater.dispatcher
                    
                    
                    def info_handler(update: Update, context: CallbackContext):
                        if str(update.effective_chat.id) != self.allowed_chat_id:
                            update.message.reply_text("⚠️ Доступ запрещён!")
                            return
                        
                        try:
                            system_info = self.get_system_info()
                            update.message.reply_text(system_info)
                        except Exception as e:
                            update.message.reply_text(f"Ошибка: {str(e)}")

                    
                    def start_handler(update: Update, context: CallbackContext):
                        if str(update.effective_chat.id) == self.allowed_chat_id:
                            update.message.reply_text(
                                "✅ Бот готов к работе!\n"
                                "Используйте /info для получения данных системы"
                            )
                        else:
                            update.message.reply_text("🚫 У вас нет доступа к этому боту")
                            
                    # def restart_terminal(update: Update, context: CallbackContext):
                    #     if str(update.effective_chat.id) == self.allowed_chat_id:
                    #         update.message.reply_text("перезапуск...")
                            

                    #         update.message.reply_text("ок.")
                    #     else:
                    #         update.message.reply_text("🚫 У вас нет доступа к этому боту")
                    def restart_dsi(update: Update, context: CallbackContext):
                        if str(update.effective_chat.id) == self.allowed_chat_id:
                            update.message.reply_text("перезапуск dsi")
                            self.display_system_info()
                                
                        else:
                            update.message.reply_text("🚫 У вас нет доступа к этому боту")
                            
                    
                    
                    
                    dispatcher.add_handler(CommandHandler("info", info_handler))
                    dispatcher.add_handler(CommandHandler("start", start_handler))
                    # dispatcher.add_handler(CommandHandler("restartterminal", restart_terminal))
                    dispatcher.add_handler(CommandHandler("restart", restart_dsi))
                    
                    
                    
                    
                    
                    updater.start_polling()
                    self.telegram_bot = updater
                    self.add_line(f"Бот запущен для чата ID: {self.allowed_chat_id}", 'normal')
                    
                    
                    
                except Exception as e:
                    self.add_line(f"Ошибка запуска бота: {str(e)}", 'highlight')

            
            threading.Thread(target=bot_thread, daemon=True).start()
    
    def get_system_info(self):
        
        temper_cpu = cputemp()
        uptime = datetime.timedelta(seconds=time.time()-psutil.boot_time())
        uptime_str = str(uptime).split('.')[0]
        
        
        
        info = [
            f"🖥️ Система: {platform.system()} {platform.release()}",
            f"⏱️ Время работы: {uptime_str}",
            f"💾 Память: {psutil.virtual_memory().percent}% used {monitor_memory()}",
            f"🔥 CPU: {psutil.cpu_percent()}% | {psutil.cpu_count()} cores, {temper_cpu}",
            f"🌐 IP: {self.get_ip_address()},",
            f"🔋 Батарея: {get_battery_info()}"  
        ]
        return "\n".join(info)
    
    def stop_bot(self):
        if not self.telegram_bot:
            self.add_line("Бот не запущен!", 'highlight')
        else:
            self.add_line("Останавливаю бота...", 'normal')
            try:
                
                temp_updater = Updater(self.bot_token)
                
                
                temp_updater.bot.send_message(
                    chat_id=self.allowed_chat_id,
                    text="🛑 Бот отключается по команде из терминала"
                )
                
                
                self.telegram_bot.stop()
                self.telegram_bot = None
                
                self.add_line("Бот успешно остановлен", 'normal')
                
            except Exception as e:
                self.add_line(f"Ошибка при остановке бота: {str(e)}", 'highlight')
            
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
        
        text = self.terminal.toPlainText()
        pos = text.rfind(prefix)
        
        if pos == -1:
            self.add_line(f"                                      |{prefix}{new_value}", color or 'normal', auto_scroll=False)
        else:
            scrollbar = self.terminal.verticalScrollBar()
            old_scroll_pos = scrollbar.value()
            
            cursor = self.terminal.textCursor()
            cursor.setPosition(pos + len(prefix))
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            
            if color:
                format = QTextCharFormat()
                format.setForeground(self.colors[color])
                cursor.setCharFormat(format)
            
            cursor.insertText(new_value)
            scrollbar.setValue(old_scroll_pos)
    
    def display_system_info(self):
        
        
        
        self.terminal.clear()
        
        os_info = f"                                      |OS: {platform.system()} {platform.release()}"
        kernel = f"                                      |Kernel: {platform.release()}"
        
        uptime = datetime.timedelta(seconds=time.time()-psutil.boot_time())
        uptime_str = str(uptime).split('.')[0]
        
        try:
            packages = subprocess.check_output(["pacman", "-Qq"]).decode().count('\n')
        except:
            packages = "N/A"
        
        shell = psutil.Process().parent().name()
        
        mem = psutil.virtual_memory()
        mem_used = mem.used / (1024**3) 
        mem_total = mem.total / (1024**3) 
        
        cpu_info = str(nameCPU[:-2])
        gpu_info = get_gpu_info()
        
        cpu_temp = cputemp()
        temperature = temp1()
        ip_address = self.get_ip_address()
        cpuresinfo = get_gpu_info_resolution()
        cheksys = check_inf_windows()
        proxy_tf = get_system_proxy()
        battery_info = get_battery_info()
        
        self.add_line("--------------------------------", 'highlight')
        self.add_line(f'{os_info}', auto_scroll=False)
        self.add_line(f'{kernel}', auto_scroll=False)
       
       
        self.update_line("Time: ", QDateTime.currentDateTime().toString("HH:mm:ss"), 'time')
        self.update_line("System: ", cheksys or "N/A", 'highlight')
        self.add_line(f"           /\     ┌──┐      ┌─┐       |Uptime: {uptime_str}", auto_scroll=False)
        self.add_line(f"          /  \    |  |      | |       |Host: {platform.node()}, {battery_info}", auto_scroll=False)    
        self.add_line(f"         / /\ \   |  |      | |       |Resolution: {cpuresinfo}", auto_scroll=False)
        self.add_line(f"        / /  \ \  |  |      | |       |Shell: {shell}", auto_scroll=False)
        self.add_line(f"       /  \__/  \ |  |      | |       |Temp: {temperature}° (outdoor)", auto_scroll=False)
        self.add_line(f"      /  /\  /\  \|  |______| |       |CPU: {cpu_info}, {cpu_temp}", auto_scroll=False)
        self.add_line(f"     /__/  \/  \__\___________|       |GPU: {gpu_info}", auto_scroll=False)
        self.update_line(f"MEM: ", monitor_memory() or "N/A", 'highlight')
        self.add_line(f"                                      |Proxy: {proxy_tf}", 'network', auto_scroll=False)
        self.add_line(f"prealph6                              |IP Address: {ip_address}", 'network', auto_scroll=False)
        self.update_line("Network name: ", self.get_network_name() or "N/A", 'highlight')
        
        
        
        
        
        # self.add_line(f"          *************               |Memory: {mem_used:.1f}GB / {mem_total:.1f}GB", auto_scroll=False)
        
        
    
    def get_ip_address(self):
        try:
            if platform.system() == "Windows":
                return subprocess.getoutput("ipconfig | findstr IPv4").split(":")[1].strip()
            else:  
                return subprocess.getoutput("hostname -I").split()[0].strip()
        except:
            return "N/A"
    
    def get_network_name(self):
        try:
            wifi_info = subprocess.getoutput("netsh wlan show interfaces | findstr SSID")
            return wifi_info.split(":")[1].strip()[:-5] if "SSID" in wifi_info else "N/A"
        except:
            return "N/A"
    
    def setup_timers(self):
        self.update_clock()
        self.update_ip_name()
        self.update_system_info()
        self.update_memory_inf()
    
    def update_clock(self):
        self.update_line("Time: ", QDateTime.currentDateTime().toString("HH:mm:ss"), 'time')
        QTimer.singleShot(1000, self.update_clock)
    
    def update_ip_name(self):
        self.update_line("Network name: ", self.get_network_name() or "N/A", 'time')
        QTimer.singleShot(60000, self.update_ip_name)
        
    def update_system_info(self):
        self.update_line("System: ", check_inf_windows() or "N/A")
        QTimer.singleShot(150000, self.update_system_info)
        
    def update_memory_inf(self):
        self.update_line("MEM: ", monitor_memory() or "N/A")
        QTimer.singleShot(5000, self.update_memory_inf)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    main_window = QMainWindow()
    main_window.setWindowFlags(Qt.FramelessWindowHint)
    main_window.setAttribute(Qt.WA_TranslucentBackground)
    main_window.resize(1000, 415)
    main_window.setStyleSheet("QMainWindow { background: transparent; }")
    
    title_bar = CustomTitleBar(main_window)
    container = QWidget()
    container.setStyleSheet("background: transparent;")
    
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.addWidget(title_bar)
    
    terminal = ArchTerminal()
    layout.addWidget(terminal)
    
    main_window.setCentralWidget(container)
    
   
    def move_window(event):
        if event.buttons() == Qt.LeftButton:
            main_window.move(event.globalPos() - title_bar.drag_pos)
    
    def mouse_press_event(event):
        if event.button() == Qt.LeftButton:
            title_bar.drag_pos = event.globalPos() - main_window.frameGeometry().topLeft()
    
    title_bar.mouseMoveEvent = move_window
    title_bar.mousePressEvent = mouse_press_event
    
    splash = SplashScreen(main_window)
    splash.show()
    
    main_window.show()
    sys.exit(app.exec_())
