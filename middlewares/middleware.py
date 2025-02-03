from collections.abc import Awaitable
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DataBaseSession(BaseMiddleware):
    """
    Мидлварь для управления асинхронной сессией базы данных в контексте обработки событий.

    Класс отвечает за создание и управление асинхронной сессией базы данных для каждого события,
    обрабатываемого ботом. Сессия автоматически добавляется в данные контекста и передается в хэндлеры,
    затем закрывается после завершения обработки события.

    :param async_session: Фабрика для создания асинхронной сессии SQLAlchemy.
    """

    def __init__(self, async_session: async_sessionmaker):
        self.async_session = async_session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """
        Создает и передает асинхронную сессию базы данных в контекст данных хэндлера.

        Метод создает асинхронную сессию и добавляет её в словарь данных (`data`), доступный хэндлеру.
        После завершения обработки события сессия автоматически закрывается.

        :param handler: Функция-хэндлер, обрабатывающая событие.
        :param event: Объект события Telegram.
        :param data: Словарь данных, передаваемых в хэндлер.
        :return: Результат выполнения хэндлера.
        """
        async with self.async_session() as session:
            data['session'] = session
            return await handler(event, data)
