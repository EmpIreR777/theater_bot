import asyncio

from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from keyboards.reply import ScenarioKeyboard


async def send_message_with_delay(
        message: Message,
        text: str,
        buttons: list | None = None,
        delay: int = 0.5,
        action: str = 'typing',
        latitude: float | None = None,
        longitude: float | None = None,
) -> object:
    """Общая функция для отправки ответа с задержкой"""
    async with ChatActionSender(
        bot=message.bot,
        chat_id=message.chat.id,
        action=action,
    ):
        await asyncio.sleep(delay)
    markup = ScenarioKeyboard(buttons).get_keyboard() if buttons else None

    await message.answer(text, reply_markup=markup)

    if latitude and longitude:
        await message.bot.send_location(
            chat_id=message.chat.id,
            latitude=latitude,
            longitude=longitude,
        )
