import uuid

from celery import shared_task

from telegram_bot.config import TelegramRedis
from telegram_bot.sender_bot.inline_keyboards import (task_link_keyboard,
                                                      task_link_and_postpone_mode_keyboard)
from telegram_bot.sender_bot.bot import bot


tr = TelegramRedis()

@shared_task(bind=True, max_retries=3)
def send_telegram_notification_before_expire_task(self, chat_id: int, message: str, task_url: str):
    """
    Сообщение о скорой просрочке задачи.
    """
    try:
        bot.send_message(chat_id, message, parse_mode="Markdown", reply_markup=task_link_keyboard(task_url))
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_telegram_notification_at_expire_task(
        self,
        chat_id: int,
        message: str,
        task_url: str,
        task_id: int
    ):
    """
    Сообщение о просрочке задачи.
    """
    callback_key = f"call:{str(uuid.uuid4())}"  # пример: "call:977ac410-f025-4009-9dba-22ff9ac4140f"
    callback_value = f"task!{task_id}!{task_url}"
    tr.set_task_callback_data(
        callback_key, callback_value
    )

    try:
        bot.send_message(
            chat_id,
            message,
            parse_mode="Markdown",
            reply_markup=task_link_and_postpone_mode_keyboard(callback_key)
        )
    except Exception as e:
        self.retry(exc=e, countdown=60)
