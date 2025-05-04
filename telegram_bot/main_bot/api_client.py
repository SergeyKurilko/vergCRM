import aiohttp
from telegram_bot.config import BotConfig

class CRMAPIClient:
    def __init__(self):
        self.base_url = BotConfig.API_BASE_URL
        self.headers = {
            "X-API-KEY": BotConfig.API_KEY,
            "Content-Type": "application/json"
        }

    async def postpone_task(self, task_id: int, period: str, telegram_id: int):
        """
        Запрос к API для переноса срока выполнения задачи.
        """
        endpoint = f"/api/tasks/{task_id}/postpone/{period}"
        url = f"{self.base_url}{endpoint}/"

        async with aiohttp.ClientSession() as session:
            async with session.patch(
                url=url,
                headers={**self.headers, "Telegram-ID": str(telegram_id)},
            ) as response:
                if response.status == 200:
                    response_dict = {
                        "status": response.status,
                        "data": await response.json()
                    }
                    return response_dict
                else:
                    return None

    async def turn_off_reminder(self, reminder_id: int, telegram_id: int):
        """
        Запрос к API для отключения напоминания.
        """
        endpoint = f"/api/reminders/{reminder_id}"
        url = f"{self.base_url}{endpoint}/"

        async with aiohttp.ClientSession() as session:
            async with session.delete(
                url=url,
                headers={**self.headers, "Telegram-ID": str(telegram_id)},
            ) as response:
                return response
