from celery import shared_task
from telegram_bot.sender_bot.bot import bot
from telegram_bot.sender_bot.inline_keyboards import task_link_keyboard

@shared_task(bind=True, max_retries=3)
def send_telegram_once_reminder(self, chat_id: int, message: str, task_url: str):
    try:
        bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="HTML",
            reply_markup=task_link_keyboard(task_url=task_url)
        )
    except Exception as e:
        self.retry(exc=e, countdown=60)