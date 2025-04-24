from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_postpone_keyboard(task_id: int, task_url: str):
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