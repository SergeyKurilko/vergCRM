from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(Path('../../.env'))

class BotConfig:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_BASE_URL = os.getenv("BASE_URL")
    API_KEY = os.getenv("X_API_KEY")
