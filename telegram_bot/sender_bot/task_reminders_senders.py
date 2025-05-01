import uuid

from celery import shared_task
from telegram_bot.sender_bot.bot import bot
from telegram_bot.sender_bot.inline_keyboards import (
    task_link_keyboard,
    task_link_and_off_recurring_reminder_mode_keyboard
)
from telegram_bot.config import TelegramRedis

tr = TelegramRedis()

@shared_task(bind=True, max_retries=3)
def send_telegram_once_reminder(self, chat_id: int, task_title: str, task_url: str):
    """
    Задача отправки разового напоминания в телеграм
    """
    message = (
        f"⏰ Напоминание о задаче: {task_title}\n"
    )

    try:
        bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="HTML",
            reply_markup=task_link_keyboard(task_url=task_url)
        )
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_telegram_recurring_reminder(
        self, chat_id: int, task_title: str,
        task_url: str, reminder_id: int
    ):
    """
    Задача отправки повторяющегося напоминания в телеграм
    """
    message = (
        f"⏰ Напоминание о задаче: {task_title}\n\n"
        f"<i>Это повторяющееся напоминание. Его можно отключить.</i>"
    )

    # Сохраняем данные в redis
    callback_key = f"call:{str(uuid.uuid4())}"  # пример: "call:977ac410-f025-4009-9dba-22ff9ac4140f"
    callback_value = f"reminder!{reminder_id}!{task_title}!{task_url}"
    tr.set_reminder_callback(
        callback_key, callback_value
    )

    try:
        bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="HTML",
            reply_markup=task_link_and_off_recurring_reminder_mode_keyboard(
                callback_key
            )
        )
    except Exception as e:
        self.retry(exc=e, countdown=60)
