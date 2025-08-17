from .terminal_plugin import Plugin
import psutil
import platform
import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import pyautogui 
import logging
import threading
from modules_plus.config import BOT_TOKEN, ID_CHAT
import time

class TelegramplusPlugin(Plugin):
    def __init__(self, terminal):
        super().__init__(terminal)
        self.bot_token = BOT_TOKEN
        self.chat_id = ID_CHAT
        self.register_command("!tc", "Настроить бота для скриншотов", self.setup_bot)
        self.updater = None

    def setup_bot(self, command: str):
        
        if not self.bot_token:
            self.terminal.add_line("❌ BOT_TOKEN не настроен", 'highlight')
            return

        if self.updater:
            self.terminal.add_line("🤖 Бот уже запущен", 'normal')
            return

        self.terminal.add_line("🔄 Запускаю бота для приема команд...", 'normal')
        
        def start_bot():
            self.updater = Updater(self.bot_token)
            dp = self.updater.dispatcher
            
            dp.add_handler(CommandHandler("screenshot", self.handle_telegram_request))
            dp.add_handler(CommandHandler("tplus", self.handle_start))
            dp.add_handler(CommandHandler("time", self.handle_time))
            
            self.updater.start_polling()
            self.terminal.add_line("✅ Бот готов принимать команды", 'normal')

        threading.Thread(target=start_bot, daemon=True).start()

    def handle_telegram_request(self, update: Update, context: CallbackContext):
        
        try:
            update.message.reply_text("🔄 Делаю скриншот...")
            
           
            screenshot = pyautogui.screenshot()
            screenshot_path = "tg_screenshot.png"
            screenshot.save(screenshot_path)
            
            with open(screenshot_path, 'rb') as photo:
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo,
                    caption="Скриншот с компьютера"
                )
            
            os.remove(screenshot_path)
            update.message.reply_text("✅ Скриншот отправлен")
        except Exception as e:
            update.message.reply_text(f"❌ Ошибка: {str(e)}")

    def handle_start(self, update: Update, context: CallbackContext):
        
        update.message.reply_text(
            "🤖 telegram+ plugin function: \n"
            "Доступные команды:\n"
            "/screenshot - получить скриншот\n"
            
        )

    def handle_time(self, update: Update, context: CallbackContext):
        t = time.time
        t = str(t) 
        update.message.reply_text(t)
        
    def get_help(self):
        return (
            "Telegram Bot Плагин:\n"
            "  !tc - Активировать бота для приема команд из Telegram\n"
            "Команды бота:\n"
            "  /screenshot - Получить скриншот\n"
           
        )