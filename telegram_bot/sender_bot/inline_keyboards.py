import uuid
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot.config import TelegramRedis

tr = TelegramRedis()

def task_link_and_postpone_mode_keyboard(task_url: str, task_id: int):
    """
    Клавиатура для перехода к задаче и входа в режим переноса срока.
    """
    callback_key = f"call:{str(uuid.uuid4())}" # пример: "call:977ac410-f025-4009-9dba-22ff9ac4140f"
    callback_value = f"task!{task_id}!{task_url}"
    tr.set_task_callback_data(
        callback_key, callback_value
    )

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Открыть задачу 🔗",
            url=task_url),
    )
    markup.row(
        InlineKeyboardButton(
            text="Перенести срок задачи",
            callback_data=f"postpone-task-mode!{callback_key}"),
    )
    return markup


def task_link_and_off_recurring_reminder_mode_keyboard(task_url: str, reminder_id):
    """
    Клавиатура для перехода к задаче из повторяющегося напоминания,
    а так же для входа в режим отключения этого напоминания.
    """
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Открыть задачу 🔗",
            url=task_url),
    )
    markup.row(
        InlineKeyboardButton(
            text="Выключить напоминание",
            callback_data=f"rem-off-mode!{reminder_id}!{task_url}"),
    )
    return markup

def task_link_keyboard(task_url: str):
    """
    Клавиатура для перехода к задаче.
    """
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Открыть задачу 🔗",
            url=task_url),
    )
    return markup