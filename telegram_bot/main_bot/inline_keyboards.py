from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_postpone_keyboard(task_id: int, task_url: str):
    """
    Клавиатура с выбором периодов переноса срока задачи.
    """
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("+1 час", callback_data=f"conf-post!hour!{task_id}!{task_url}"),
        InlineKeyboardButton("+3 часа", callback_data=f"conf-post!three_hour!{task_id}!{task_url}")
    )
    markup.row(
        InlineKeyboardButton("+1 день", callback_data=f"conf-post!day!{task_id}!{task_url}"),
        InlineKeyboardButton("+1 неделя", callback_data=f"conf-post!week!{task_id}!{task_url}")
    )
    markup.row(
        InlineKeyboardButton("Отмена", callback_data=f"cancel-postpone-mode!{task_id}!{task_url}")
    )
    return markup


def off_reminder_keyboard(reminder_id: int, task_url: str):
    """
    Клавиатура для подтверждения отключения напоминания.
    """
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Да, отключить напоминание.",
            callback_data=f"conf-rem-off!{reminder_id}"
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Нет, оставить напоминание.",
            callback_data=f"cancel-rem-off!{reminder_id}!{task_url}"
        )
    )
    return markup