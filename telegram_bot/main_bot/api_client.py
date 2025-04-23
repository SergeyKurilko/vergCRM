import aiohttp
from telegram_bot.main_bot.config import BotConfig

class CRMAPIClient:
    def __init__(self):
        self.base_url = BotConfig.API_BASE_URL
        self.headers = {
            "X-API-KEY": BotConfig.API_KEY,
            "Content-Type": "application/json"
        }

    async def postpone_task(self, task_id: int, period: str, telegram_id: int):
        # /api/tasks/382/postpone/hour/
        endpoint = f"/api/tasks/{task_id}/postpone/{period}"
        url = f"{self.base_url}{endpoint}"

        async with aiohttp.ClientSession() as session:
            async with session.patch(
                url=url,
                headers={**self.headers, "Telegram-ID": str(telegram_id)},
            ) as response:
                return await response.json()