from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.models import Coupon


class CRUDCoupons(CRUDBase):
    async def get_by_code(self, number: str, session: AsyncSession):
        """Получить купон по его коду."""
        condition = (self.model.code == number) & (self.model.is_active == True)  # noqa: E712
        return await self._fetch_one(condition, session)

    async def deactivate(self, number: str, session: AsyncSession):
        """Деактивировать купон по номеру."""
        db_obj = await self.get_by_code(number, session)

        if db_obj:
            db_obj.is_active = False
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj


crud_coupons = CRUDCoupons(Coupon)
