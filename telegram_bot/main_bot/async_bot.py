import asyncio
import os
import sys

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent.parent.parent  # Переходим из telegram_bot/main_bot в vergCRM
sys.path.append(str(project_root))

from telegram_bot.main_bot.task_handlers import (handler_get_keyboard_for_postpone_task,
                                                 handler_cancel_postpone_mode,
                                                 handler_confirm_postpone_task,
                                                 handler_enter_to_off_reminder_mode,
                                                 handler_exit_from_off_reminder_mode,
                                                 handler_confirm_off_reminder)

load_dotenv(Path('../../.env'))
TELEGRAM_BOT_TOKEN=os.getenv("BOT_TOKEN")


# Основной бот для работы с API
bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(func=lambda message: message.text.startswith("admin_test"))
async def test_message_echo(message: Message):
    """Отслеживание тестового сообщения"""
    await bot.reply_to(message, text="Бот запущен и работает.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('postpone-task-mode!'))
async def callback_enter_to_postpone_task_mode(call: CallbackQuery):
    """
    Отслеживание нажатия inline кнопки "Перенести срок задачи".
    """
    await handler_get_keyboard_for_postpone_task(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel-postpone-mode!'))
async def callback_cancel_postpone_task_mode(call: CallbackQuery):
    """
    Отслеживание нажатия inline кнопки "Отмена" при выборе периода переноса срока задачи.
    """
    await handler_cancel_postpone_mode(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('conf-post!'))
async def callback_confirm_postpone_task(call: CallbackQuery):
    """
    Отслеживание нажатия кнопок с периодами переноса срока задачи (+1 час, +1 день и т.д.)
    """
    await handler_confirm_postpone_task(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('rem-off-mode!'))
async def callback_enter_to_off_reminder_mode(call: CallbackQuery):
    """
    Отслеживание нажатия inline кнопки "Выключить напоминание" в сообщении с повторяющимся напоминанием.
    """
    await handler_enter_to_off_reminder_mode(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel-rem-off!'))
async def callback_enter_to_off_reminder_mode(call: CallbackQuery):
    """
    Отслеживание нажатия inline кнопки "Нет, оставить напоминание." при отключении напоминания.
    """
    await handler_exit_from_off_reminder_mode(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('conf-rem-off!'))
async def callback_confirm_off_reminder(call: CallbackQuery):
    """
    Отслеживание нажатия inline кнопки "Да, отключить напоминание." при отключении напоминания.
    """
    await handler_confirm_off_reminder(bot, call)


async def run_bot():
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(run_bot())