import os
import django
import telebot
from django.conf import settings

# Инициализация django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vergCRM.settings')
# Загрузка django
django.setup()


# Импорт моделей после инициализации django
from crm.models import UserProfile

# Создание экземпляра бота
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
