from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def task_link_and_postpone_mode_keyboard(task_url: str, task_id: int):
    """
    Клавиатура для перехода к задаче и входа в режим переноса срока.
    """
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Открыть задачу 🔗",
            url=task_url),
    )
    markup.row(
        InlineKeyboardButton(
            text="Перенести срок задачи",
            callback_data=f"postpone-task-mode!{task_id}!{task_url}"),
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