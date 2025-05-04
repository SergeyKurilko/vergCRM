import asyncio
import os
import sys
from functools import wraps

import aiohttp
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, Update
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent.parent.parent  # Переходим из telegram_bot/main_bot в vergCRM
sys.path.append(str(project_root))

from telegram_bot.config import TelegramRedis
from telegram_bot.config import BotConfig
from telegram_bot.main_bot.api_client import CRMAPIClient
from telegram_bot.main_bot.task_handlers import (handler_get_keyboard_for_postpone_task,
                                                 handler_cancel_postpone_mode,
                                                 handler_confirm_postpone_task,
                                                 handler_enter_to_off_reminder_mode,
                                                 handler_exit_from_off_reminder_mode,
                                                 handler_confirm_off_reminder)


TELEGRAM_BOT_TOKEN=BotConfig.BOT_TOKEN


api = CRMAPIClient()

# Основной бот для работы с API
bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)

# Декоратор для проверки доступа к боту:
def check_access(func):
    """
    Декоратор для проверки доступа к боту (наличие пользователя в БД)
    """
    @wraps(func)
    async def wrapped(update: Message | CallbackQuery, *args, **kwargs):
        telegram_id = update.from_user.id

        # Асинхронный запрос к API
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"{api.base_url}/api/check_telegram_access/{telegram_id}/",
                        headers=api.headers
                ) as response:
                    data = await response.json()
                    allowed = response.status == 200 and data.get("allowed", False)

                    if not allowed:
                        text = "❌ Доступ запрещён."
                        if isinstance(update, Message):
                            await bot.reply_to(update, text=text)
                        elif isinstance(update, CallbackQuery):
                            await bot.answer_callback_query(
                                callback_query_id=update.id, text=text, show_alert=True
                            )
                        return
        except Exception as e:
            text = "⚠️ Ошибка проверки доступа. Попробуйте позже."
            if isinstance(update, Message):
                await bot.reply_to(update, text=text)
            elif isinstance(update, CallbackQuery):
                await bot.answer_callback_query(
                    callback_query_id=update.id, text=text, show_alert=True
                )
            return
        return await func(update, *args, **kwargs)
    return wrapped

@bot.message_handler(func=lambda m: True)
@check_access
async def all_messages(update: Update):
    """Любые сообщения проходят через декоратор check_access"""
    pass

@bot.message_handler(func=lambda message: message.text.startswith("admin_test"))
async def test_message_echo(message: Message):
    """Отслеживание тестового сообщения"""
    await bot.reply_to(message, text="Бот запущен и работает.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('postpone-task-mode!'))
# @check_access
async def callback_enter_to_postpone_task_mode(call: CallbackQuery):
    """
    Отслеживание нажатия inline кнопки "Перенести срок задачи".
    """
    await handler_get_keyboard_for_postpone_task(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel-p!'))
async def callback_cancel_postpone_task_mode(call: CallbackQuery):
    """
    Отслеживание нажатия inline кнопки "Отмена" при выборе периода переноса срока задачи.
    """
    await handler_cancel_postpone_mode(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('c-p!'))
@check_access
async def callback_confirm_postpone_task(call: CallbackQuery):
    """
    Отслеживание нажатия кнопок с периодами переноса срока задачи (+1 час, +1 день и т.д.)
    """
    await handler_confirm_postpone_task(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('rem-off-mode!'))
@check_access
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
@check_access
async def callback_confirm_off_reminder(call: CallbackQuery):
    """
    Отслеживание нажатия inline кнопки "Да, отключить напоминание." при отключении напоминания.
    """
    await handler_confirm_off_reminder(bot, call)


async def run_bot():
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(run_bot())