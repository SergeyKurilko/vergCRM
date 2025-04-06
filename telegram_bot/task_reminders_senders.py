from celery import shared_task


@shared_task(bind=True, max_retries=3)
def send_telegram_reminder(self, chat_id: int, message: str):
    try:
        from telegram_bot.bot import bot  # Импорт здесь, чтобы не грузить при старте
        bot.send_message(chat_id, message, parse_mode="Markdown")
    except Exception as e:
        self.retry(exc=e, countdown=60)