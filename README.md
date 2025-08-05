
# arch-LInux-terminal-by-ultimate-for-windows, prealphver06
![Terminal Screenshot](scrns.png) 

## *ru* 
Терминал в стиле Arch Linux для Windows с мониторингом показателей и интегрированным Telegram-ботом

## 🔥 Основные функции
- Аутентичный интерфейс Arch Linux
- Комплексный мониторинг (CPU/RAM/сеть/батарея)
- Встроенный Telegram-бот для удаленного доступа (в будущем удалённое управление через Telegram-бота)
- Полноценная командная строка(Поддержка обычных команд cd, clear и др.)
- Гибкая система команд

## 🚀 фаст старт

1. Установите зависимости:
pip install PyQt5 psutil python-telegram-bot python-dotenv requests wmi

2. Настройка:
- Создайте .env файл:
- BOT_TOKEN=ваш_токен_бота
- ALLOWED_CHAT_ID=ваш_id_в_телеграмме
- Для погоды отредактируйте: modules_plus/weather.py -> CITY = "Ваш город" (в будущем переедет в .env)

3. Запуск:
python "arch Linux main.py"
  
## 📊 Мониторинг системы

Требования: OpenHardwareMonitor для температуры CPU

Частота обновления:
- Время: 1 сек
- RAM: 5 сек
- Система/Сеть: 60 сек

## 📚 Используемые библиотеки/требования:
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

**📌 Проект находится в активной разработке.**



## *en*
Arch Linux-style terminal for Windows with system monitoring and Telegram bot

## 🔥 Main features
- Authentic Arch Linux interface
- Comprehensive monitoring (CPU/RAM/network/battery)
- Built-in Telegram bot for remote access (future remote control via Telegram bot)
- Full-fledged command line (Support for common commands cd, clear etc.)

Flexible command system

## 🚀 Quick start

1. Install dependencies:
pip install PyQt5 psutil python-telegram-bot python-dotenv requests wmi

2. Setup:
Create .env file:
BOT_TOKEN=your_bot_token
ALLOWED_CHAT_ID=your_chat_id
For weather edit: modules_plus/weather.py -> CITY = "Your city"

3. Launch:
python "arch Linux main.py"
  
## 📊 System monitoring

Requirements: OpenHardwareMonitor for CPU temperature

Update frequency:
Time: 1 sec
RAM: 5 sec
System/Network: 60 sec

## 📚 Used libraries/requirements:
PyQt5, platform, psutil, datetime, time, 
subprocess, requests, winreg, wmi, os, 
socket, sys, python-telegram-bot, python-dotenv

*Python 3.12.4+ | Windows 10/11*
**Administrator rights required for full functionality**

## 📅 Version history:
prealpha-v0.1 (24.07.2025): Core logic

prealpha-v0.2 (26.07.2025): Command line

prealpha-v0.3 (27.07.2025): Telegram bot

prealpha-v0.4 (28.07.2025): Logging

prealpha-v0.5 (31.07.2025): Revised tg connection logic + commandline logic changes

**📌 Project is under active development.**


