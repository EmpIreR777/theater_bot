from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import TgUser


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def _fetch_one(self, condition, session: AsyncSession):
        """Возвращает первый объект, соответствующий условию, либо None, если таких объектов нет."""
        stmt = select(self.model).where(condition)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get(self, obj_id: int, session: AsyncSession):
        return await self._fetch_one(self.model.id == obj_id, session)

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ):
        attr = getattr(self.model, attr_name)
        return await self._fetch_one(attr == attr_value, session)

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in, session: AsyncSession):
        obj_in_data = obj_in

        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj


crud_tg_user = CRUDBase(model=TgUser)
