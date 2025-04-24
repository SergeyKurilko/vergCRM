import os
from pathlib import Path
from dotenv import load_dotenv
from telebot import TeleBot  # Синхронная версия!

load_dotenv(Path('../../.env'))
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")

# Синхронный бот только для отправки сообщений
bot = TeleBot(TELEGRAM_BOT_TOKEN)
