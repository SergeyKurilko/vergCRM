from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.config import TelegramRedis

tr = TelegramRedis()

def create_postpone_keyboard(callback_key):
    """
    Клавиатура с выбором периодов переноса срока задачи.
    """
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("+1 час", callback_data=f"c-p!hour!{callback_key}"),
        InlineKeyboardButton("+3 часа", callback_data=f"c-p!three_hour!{callback_key}")
    )
    markup.row(
        InlineKeyboardButton("+1 день", callback_data=f"c-p!day!{callback_key}"),
        InlineKeyboardButton("+1 неделя", callback_data=f"c-p!week!{callback_key}")
    )
    markup.row(
        InlineKeyboardButton("Отмена", callback_data=f"cancel-p!{callback_key}")
    )
    return markup


def off_reminder_keyboard(callback_key):
    """
    Клавиатура для подтверждения отключения напоминания.
    """

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Да, отключить напоминание.",
            callback_data=f"conf-rem-off!{callback_key}"
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Нет, оставить напоминание.",
            callback_data=f"cancel-rem-off!{callback_key}"
        )
    )
    return markup