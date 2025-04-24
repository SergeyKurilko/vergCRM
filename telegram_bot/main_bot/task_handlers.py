from datetime import datetime

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telebot.async_telebot import AsyncTeleBot
from telegram_bot.main_bot.api_client import CRMAPIClient
from telegram_bot.main_bot.inline_keyboards import (
    create_postpone_keyboard,
    off_reminder_keyboard)
from telegram_bot.sender_bot.inline_keyboards import (
    task_link_and_postpone_mode_keyboard,
    task_link_keyboard,
    task_link_and_off_recurring_reminder_mode_keyboard
)

api = CRMAPIClient()


async def handler_get_keyboard_for_postpone_task(bot: AsyncTeleBot, call: CallbackQuery):
    """
    Присваивает состояние ожидания срока переноса задачи, возвращает клавиатуру для выбора срока или отмены.
    """
    call_data = call.data.split('!')

    task_id = int(call_data[1])
    task_url = call_data[2]

    keyboard_for_select_postpone = create_postpone_keyboard(
        task_id=task_id,
        task_url=task_url
    )

    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=keyboard_for_select_postpone
    )


async def handler_confirm_postpone_task(bot: AsyncTeleBot, call: CallbackQuery):
    """
    Подтверждение переноса срока просроченной задачи. Запрос к API-endpoint для изменения срока.
    Пример приходящего call.data: "confirm-postpone_week_{task_id}"
    """
    call_data = call.data.split('!')
    telegram_id = call.from_user.id
    period = call_data[1]
    task_id = int(call_data[2])
    task_url = call_data[3]

    original_message_text = call.message.text

    # Пока делается запрос показываем паузу
    await bot.edit_message_text(
        text=f"{original_message_text}\n\n <b>Подождите. Ищу задачу... </b> 🔍",
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=None,
        parse_mode="HTML",
    )

    api_response = await api.postpone_task(
        task_id=task_id,
        period=period,
        telegram_id=telegram_id
    )

    if api_response and api_response.get("status") == 200:
        new_date_str = api_response["data"]["must_be_completed_by"]

        # Парсим строку в объект datetime
        date_obj = datetime.fromisoformat(new_date_str)
        # Форматируем дату в нужный формат
        new_date = date_obj.strftime("%d.%m.%Yг. (до %H:%M)")

        await bot.edit_message_text(
            text=f"{original_message_text}\n\n <b>Срок задачи перенесен. Новая дата: {new_date}</b>",
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=task_link_keyboard(task_url=task_url),
            parse_mode="HTML",
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="Ошибка.",
            show_alert=True
        )


async def handler_cancel_postpone_mode(bot: AsyncTeleBot, call: CallbackQuery):
    """
    Отмена выбора переноса срока просроченной задачи
    """
    call_data = call.data.split('!')

    task_id = int(call_data[1])
    task_url = call_data[2]

    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=task_link_and_postpone_mode_keyboard(
            task_url=task_url,
            task_id=task_id
        )
    )


async def handle_task_postpone(bot: AsyncTeleBot, call):
    """
    Отправляет запрос на API для переноса срока задачи.
    """
    _, period, task_id = call.data.split(':')
    telegram_id = call.from_user.id

    try:
        response = await api.postpone_task(
            task_id=int(task_id),
            period=period,
            telegram_id=telegram_id
        )

        if response.get('success'):
            await bot.answer_callback_query(
                call.id,
                f"Срок задачи перенесен на {period.replace('_', ' ')}!",
                show_alert=True
            )
        else:
            await bot.answer_callback_query(
                call.id,
                "Ошибка: " + response.get('error', 'Неизвестная ошибка'),
                show_alert=True
            )
    except Exception as e:
        await bot.answer_callback_query(
            call.id,
            f"Ошибка соединения: {str(e)}",
            show_alert=True
        )


async def handler_enter_to_off_reminder_mode(
        bot: AsyncTeleBot, call: CallbackQuery
):
    """
    Вход в режим отключения повторяющегося напоминания.
    Возвращает клавиатуру для подтверждения отключения или отмены.
    """
    call_data = call.data.split('!')
    reminder_id = int(call_data[1])
    task_url = call_data[2]
    original_message_text = call.message.text

    await bot.edit_message_text(
        text=f"{original_message_text} \n\n "
             f"🟢 🟢 🟢 🟢 🟢 🟢 \n\n"
             f"<b>Подтвердите отключение напоминания.</b>",
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode="HTML",
        reply_markup=off_reminder_keyboard(reminder_id=reminder_id, task_url=task_url)
    )


async def handler_exit_from_off_reminder_mode(
        bot: AsyncTeleBot, call: CallbackQuery
    ):
    """
    Выход из режима отключения повторяющегося напоминания.
    """
    call_data = call.data.split('!')
    reminder_id = int(call_data[1])
    task_url = call_data[2]
    original_message_text = call.message.text.split("🟢")[0].rstrip()

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode="HTML",
        text=original_message_text,
        reply_markup=task_link_and_off_recurring_reminder_mode_keyboard(
            reminder_id=reminder_id,
            task_url=task_url
        )
    )


async def handler_confirm_off_reminder(
    bot: AsyncTeleBot, call: CallbackQuery
    ):
    """
    Отправляет запрос для отключения повторяющегося напоминания.
    """
    # в call data: "conf-rem-off!{reminder_id}"
    call_data = call.data.split('!')
    reminder_id = int(call_data[1])
    telegram_id = call.from_user.id

    try:
        response = await api.turn_off_reminder(
            reminder_id=reminder_id,
            telegram_id=telegram_id
        )

        if response.status == 204:
            await bot.answer_callback_query(
                callback_query_id=call.id,
                text=f"Напоминание отключено успешно.",
                show_alert=True
            )
            await bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.id
            )
        else:
            await bot.answer_callback_query(
                call.id,
                "Что-то пошло не так.",
                show_alert=True
            )
    except Exception as e:
        await bot.answer_callback_query(
            call.id,
            f"Ошибка соединения: {str(e)}",
            show_alert=True
        )