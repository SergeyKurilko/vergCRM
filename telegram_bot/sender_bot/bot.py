import os
from pathlib import Path
from dotenv import load_dotenv
from telebot import TeleBot  # Синхронная версия!
from telegram_bot.config import BotConfig

# Синхронный бот только для отправки сообщений
bot = TeleBot(BotConfig.BOT_TOKEN)
