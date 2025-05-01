import uuid
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot.config import TelegramRedis

tr = TelegramRedis()

def task_link_and_postpone_mode_keyboard(callback_key):
    """
    Клавиатура для перехода к задаче и входа в режим переноса срока.
    """
    task_data = tr.get_task_callback(callback_key).split("!") # Пример данных: task!{task_id}!{task_url}
    task_url = task_data[2]

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


def task_link_and_off_recurring_reminder_mode_keyboard(callback_key):
    """
    Клавиатура для перехода к задаче из повторяющегося напоминания,
    а так же для входа в режим отключения этого напоминания.
    """

    # Пример данных в reminder_data: "reminder!{reminder_id}!{task_title}!{task_url}"
    reminder_data = tr.get_reminder_callback(callback_key).split("!")

    task_url = reminder_data[-1]

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Открыть задачу 🔗",
            url=task_url),
    )
    markup.row(
        InlineKeyboardButton(
            text="Выключить напоминание",
            callback_data=f"rem-off-mode!{callback_key}"),
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