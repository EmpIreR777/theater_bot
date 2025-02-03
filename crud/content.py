from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.models import GeoLocation, Sleep, Text, Track


class CRUDContent(CRUDBase):
    """Базовый CRUD для контента"""

    async def get_by_title(self, title: str, session: AsyncSession):
        """Получить объект по заголовку"""
        return await self.get_by_attribute('title', title, session)


class CRUDTrack(CRUDContent):
    """CRUD для треков"""

    async def get_audio(self, title: str, session: AsyncSession):
        """Получить аудиофайл трека по названию"""
        track = await self.get_by_title(title, session)
        return track.audio if track else None

    async def get_photo(self, title: str, session: AsyncSession):
        """Получить изображение трека по названию"""
        track = await self.get_by_title(title, session)
        return track.photo if track else None

    async def get_animations(self, title: str, session: AsyncSession):
        """Получить анимации трека по названию"""
        track = await self.get_by_title(title, session)
        return track.animation if track else None


class CRUDText(CRUDContent):
    """CRUD для текстов"""


class CRUDLocation(CRUDContent):
    """CRUD для геолокаций"""


class CRUDSleep(CRUDContent):
    """CRUD для пауз"""


crud_track = CRUDTrack(Track)
crud_text = CRUDText(Text)
crud_geo = CRUDLocation(GeoLocation)
crud_sleep = CRUDSleep(Sleep)
