from .terminal_plugin import Plugin
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import pyautogui 
import threading
import time
import os
import platform 
from datetime import datetime
import psutil


class TelegramPlugin(Plugin):
    def __init__(self, terminal):
        super().__init__(terminal)
        self.bot_token = None
        self.chat_id = None
        self.updater = None
        self.running = False
        
        self.register_command("tgstart", "Запустить Telegram бота", self.start_bot)
        self.register_command("tgstop", "Остановить Telegram бота", self.stop_bot)

    def start_bot(self, command: str):
        
        try:
            
            try:
                from config import BOT_TOKEN, ID_CHAT
                self.bot_token = BOT_TOKEN
                self.chat_id = ID_CHAT
            except:
                self.terminal.add_line("❌ Не найден config.py с настройками бота", 'error')
                return

            if self.running:
                self.terminal.add_line("🤖 Бот уже запущен", 'normal')
                return

            self.terminal.add_line("🔄 Запускаю Telegram бота...", 'normal')
            
            
            def bot_thread():
                try:
                    self.updater = Updater(self.bot_token)
                    dp = self.updater.dispatcher
                    
                    dp.add_handler(CommandHandler("start", self.cmd_start))
                    dp.add_handler(CommandHandler("screen", self.cmd_screenshot))
                    dp.add_handler(CommandHandler("time", self.cmd_time))
                    dp.add_handler(CommandHandler("help", self.cmd_help))
                    dp.add_handler(CommandHandler("inf", self.cmd_get_system_info))
                    
                    self.updater.start_polling()
                    self.running = True
                    self.terminal.add_line("✅ Бот запущен! Команды: /start, /screen, /time", 'normal')      
                    
                    while self.running:
                        time.sleep(1)
                        
                except Exception as e:
                    self.terminal.add_line(f"❌ Ошибка бота: {str(e)}", 'error')
                    self.running = False

            thread = threading.Thread(target=bot_thread, daemon=True)
            thread.start()
            
        except Exception as e:
            self.terminal.add_line(f"❌ Ошибка: {str(e)}", 'error')

    def stop_bot(self, command: str):
       
        if not self.running:
            self.terminal.add_line("🤖 Бот не запущен", 'normal')
            return
            
        try:
            if self.updater:
                self.updater.stop()
            self.running = False
            self.terminal.add_line("🛑 Бот остановлен", 'normal')
        except:
            self.terminal.add_line("⚠️ Бот остановлен с ошибкой", 'error')
            self.running = False

    def cmd_start(self, update: Update, context: CallbackContext):
        
        update.message.reply_text(
            "🤖 Бот активирован!\n"
            "Доступные команды:\n"
            "/screen - Скриншот экрана\n"
            "/time - Время системы\n"
            "/help - Помощь"
        )

    def cmd_screenshot(self, update: Update, context: CallbackContext):
        try:
            self.terminal.add_line('[ATTENTION] - screenshot', 'attention')
            update.message.reply_text("📸 Делаю скриншот...")
            
            screenshot = pyautogui.screenshot()
            screenshot.save("screen.png")
            
            with open("screen.png", 'rb') as photo:
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo,
                    caption="Скриншот",
                )
            
            os.remove("screen.png")
            
        except Exception as e:
            update.message.reply_text(f"❌ Ошибка: {str(e)}")

    def cmd_time(self, update: Update, context: CallbackContext):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        update.message.reply_text(f"🕒 Время системы: {current_time}")
        
        
    def cmd_get_system_info(self, update: Update, context: CallbackContext):
       
        try:
           
            from PyQt5.QtCore import QTimer, QDateTime
            uptime = QDateTime.currentDateTime().toString("HH:mm:ss")
            uptime_str = str(uptime).split('.')[0]
            
           
            battery_info = "N/A"
            try:
                battery = psutil.sensors_battery()
                if battery:
                    battery_info = f"{battery.percent}%"
                    if battery.power_plugged:
                        battery_info += " 🔌"
                    else:
                        battery_info += " 🔋"
            except:
                pass
            
            
            memory = psutil.virtual_memory()
            memory_info = f"{memory.percent}% ({memory.used//1024//1024}MB/{memory.total//1024//1024}MB)"
            
            
            cpu_info = f"{psutil.cpu_percent()}%"
            
            info = [
                f"🖥️ {platform.system()} {platform.release()}",
                f"⏱️ Uptime: {uptime_str}",
                f"🧠 CPU: {cpu_info}",
                f"💾 Memory: {memory_info}",
                f"🔋 Battery: {battery_info}",
                f"👤 User: {os.getlogin() if hasattr(os, 'getlogin') else 'N/A'}"
            ]
            
            system_info = "\n".join(info)
            update.message.reply_text(system_info)
            
        except Exception as e:
            update.message.reply_text(f"❌ Error: {str(e)}")

    def cmd_help(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "🤖 Помощь по командам:\n"
            "/start - Запуск бота\n"
            "/screen - Скриншот экрана\n"
            "/time - Время системы\n"
            "/help - Эта справка"
        )

    def get_help(self):
        return (
            "Telegram Bot:\n"
            "  tgstart - Запустить бота\n"
            "  tgstop  - Остановить бота\n"
            "Команды в Telegram:\n"
            "  /start  - Запуск\n"
            "  /screen - Скриншот\n"
            "  /time   - Время системы\n"
            "  /help   - Справка"
        )