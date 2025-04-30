from pathlib import Path
from dotenv import load_dotenv
import redis
import os

load_dotenv(Path('../../.env'))
r = redis.Redis(db=5)

class BotConfig:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_BASE_URL = os.getenv("BASE_URL")
    API_KEY = os.getenv("X_API_KEY")


class TelegramRedis:
    """
    Управление записями в redis для работы бота.
    """
    @staticmethod
    def set_task_callback_data(callback_key, callback_value):
        """Сохранение данных о задаче в redis"""
        r.setex(name=callback_key, time=259200, value=callback_value)

    def get_task_callback(self, callback_key):
        """
        Получение данных о задаче в декодированном виде (изначально возвращается b"тут_данные")
        """
        return r.get(name=callback_key).decode("utf-8")


    def get_reminder_callback(self):
        """
        Получение данных о reminder
        """
        pass

    def check_key_exists(self, callback_key):
        print(f"Тип данных в callback_key: {type(callback_key)}")
        return r.exists(callback_key)


