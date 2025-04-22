import asyncio
import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from pathlib import Path

load_dotenv(Path('../../.env'))
TELEGRAM_BOT_TOKEN=os.getenv("BOT_TOKEN")

# Основной бот для работы с API
bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)

async def run_bot():
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(run_bot())