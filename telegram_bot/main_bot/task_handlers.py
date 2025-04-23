from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telebot.async_telebot import AsyncTeleBot
from telegram_bot.main_bot.api_client import CRMAPIClient
from telegram_bot.main_bot.inline_keyboards import create_postpone_keyboard
from telegram_bot.sender_bot.inline_keyboards import task_link_and_postpone_mode_keyboard

api = CRMAPIClient()


async def handler_get_keyboard_for_postpone_task(bot: AsyncTeleBot, call: CallbackQuery):
    """
    Присваивает состояние ожидания срока переноса задачи, возвращает клавиатуру для выбора срока или отмены.
    """
    call_data = call.data.split('_')
    print(f"call_data: {call_data}")

    task_id = int(call_data[1])
    task_url = call_data[2]

    keyboard_for_select_postpone=create_postpone_keyboard(
        task_id=task_id,
        task_url=task_url
    )

    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=keyboard_for_select_postpone
    )

async def handler_cancel_postpone_mode(bot: AsyncTeleBot, call: CallbackQuery):
    """
    Отмена выбора переноса срока просроченной задачи
    """
    call_data = call.data.split('_')

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