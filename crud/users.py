import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.models import User


class CRUDUser(CRUDBase):
    async def get_user(self, username: str, password: str, session: AsyncSession):
        try:
            result = await session.execute(
                select(self.model).where(
                    self.model.username == username,
                    self.model.password == password,
                ),
            )
            user = result.scalars().first()
            logging.info(f'Пользователь {user.username} получен')
            return user

        except SQLAlchemyError as e:
            logging.exception(f'Ошибка при получении пользователей: {e}')
            raise


crud_user = CRUDUser(User)
