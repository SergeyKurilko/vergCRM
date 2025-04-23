from celery import shared_task

from telegram_bot.sender_bot.inline_keyboards import (task_link_keyboard,
                                                      task_link_and_postpone_mode_keyboard)
from telegram_bot.sender_bot.bot import bot


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
    try:
        bot.send_message(
            chat_id,
            message,
            parse_mode="Markdown",
            reply_markup=task_link_and_postpone_mode_keyboard(task_url, task_id)
        )
    except Exception as e:
        self.retry(exc=e, countdown=60)
