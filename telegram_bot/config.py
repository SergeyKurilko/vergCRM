from pathlib import Path
from dotenv import load_dotenv
import redis
import os

# Абсолютный путь к .env
ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(ENV_PATH)

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

    @staticmethod
    def set_reminder_callback(callback_key, callback_value):
        """Сохранение данных о задаче в redis"""
        r.setex(name=callback_key, time=259200, value=callback_value)

    def get_reminder_callback(self, callback_key):
        """Получение данных о reminder"""
        return r.get(name=callback_key).decode("utf-8")

    def check_key_exists(self, callback_key):
        """
        Проверка существования ключа в redis (TTL 259200 сек = 3 дня)
        """
        return r.exists(callback_key)

    @staticmethod
    def delete_key(callback_key):
        """Удаление ненужного ключа"""
        r.delete(callback_key)
        
