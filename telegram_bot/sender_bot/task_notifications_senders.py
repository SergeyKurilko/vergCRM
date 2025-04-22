from celery import shared_task
from telegram_bot.sender_bot.bot import bot


@shared_task(bind=True, max_retries=3)
def send_telegram_notification(self, chat_id: int, message: str):
    try:
        bot.send_message(chat_id, message, parse_mode="Markdown")
    except Exception as e:
        self.retry(exc=e, countdown=60)
