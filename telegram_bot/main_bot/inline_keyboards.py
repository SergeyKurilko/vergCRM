from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_postpone_keyboard(task_id: int, task_url: str):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("+1 час", callback_data=f"conf-post_hour_{task_id}_{task_url}"),
        InlineKeyboardButton("+3 часа", callback_data=f"conf-post_three-hour_{task_id}_{task_url}")
    )
    markup.row(
        InlineKeyboardButton("+1 день", callback_data=f"conf-post_day_{task_id}_{task_url}"),
        InlineKeyboardButton("+1 неделя", callback_data=f"conf-post_week_{task_id}_{task_url}")
    )
    markup.row(
        InlineKeyboardButton("Отмена", callback_data=f"cancel-postpone-mode_{task_id}_{task_url}")
    )
    return markup