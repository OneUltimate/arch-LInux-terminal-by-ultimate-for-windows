# arch-LInux-terminal-by-ultimate-for-windows, prealphver05
![Terminal Screenshot](scrns.png) 

*ru* 
Терминал в стиле Arch Linux для Windows с мониторингом системы и Telegram-ботом

## 🔥 Основные функции
Аутентичный интерфейс Arch Linux
Комплексный мониторинг (CPU/RAM/сеть/батарея)
Удалённое управление через Telegram-бота
Полноценная командная строка

Гибкая система команд

## 🚀 Быстрый старт

1. Установите зависимости:
pip install PyQt5 psutil python-telegram-bot python-dotenv requests wmi

2. Настройка:
Создайте .env файл:
BOT_TOKEN=ваш_токен_бота
ALLOWED_CHAT_ID=ваш_chat_id
Для погоды отредактируйте: modules_plus/weather.py -> CITY = "Ваш город"

3. Запуск:
python "arch Linux main.py"
  
## 📊 Мониторинг системы

Требования: OpenHardwareMonitor для температуры CPU

Частота обновления:
Время: 1 сек
RAM: 5 сек
Система/Сеть: 60 сек

## 📚 Используемые библеотеки/требования:
PyQt5, platform, psutil, datetime, time, 
subprocess, requests, winreg, wmi, os, 
socket, sys, python-telegram-bot, python-dotenv

*Python 3.12.4+ | Windows 10/11*
**Для полного функционала требуются права администратора**

## 📅 История версий:
prealpha-v0.1 (24.07.2025): Базовая логика

prealpha-v0.2 (26.07.2025): Командная строка

prealpha-v0.3 (27.07.2025): Telegram-бот

prealpha-v0.4 (28.07.2025): Логирование

prealpha-v0.5 (31.07.2025): Переработана логика подключения к tg + изменения логики commandline


