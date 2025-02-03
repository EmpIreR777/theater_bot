import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import case, func, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.models import GeneralStatistics, TgUser, TrackStatistics


class CRUDStatistics(CRUDBase):
    def __init__(self, general_model, track_model, user_model):
        self.model = user_model
        self.general_model = general_model
        self.track_model = track_model

    async def get_user_statistics(self, session: AsyncSession):
        """
        Метод собирает данные о количестве пользователей,
        зарегистрированных за различные временные периоды.
        """
        try:
            now = datetime.now(UTC)
            query = select(
                func.count().label('total_users'),
                func.sum(
                    case((self.model.create_at >= now - timedelta(days=1), 1), else_=0),
                ).label('new_today'),
                func.sum(
                    case((self.model.create_at >= now - timedelta(days=7), 1), else_=0),
                ).label('new_week'),
                func.sum(
                    case(
                        (self.model.create_at >= now - timedelta(days=30), 1), else_=0
                    ),
                ).label('new_month'),
            )
            result = await session.execute(query)
            stats = result.fetchone()
            statistics = {
                'total_users': stats.total_users,
                'new_today': stats.new_today,
                'new_week': stats.new_week,
                'new_month': stats.new_month,
            }
            logging.info(f'Статистика успешно получена: {statistics}')
            return statistics

        except SQLAlchemyError as e:
            logging.exception(f'Ошибка при получении статистики: {e}')
            raise

    async def get_scenario_statistics(self, session: AsyncSession) -> dict[str, int]:
        """Возвращает общую статистику и статистику по трекам в виде плоского словаря."""
        general_stats = await session.execute(select(self.general_model))
        general_stats = general_stats.scalars().first()

        track_stats = await session.execute(select(self.track_model))
        track_stats = track_stats.scalars().all()

        stats = {
            'users_count': general_stats.users_count,
            'started_count': general_stats.started_count,
            'finished_count': general_stats.finished_count,
        }

        for track in track_stats:
            stats[f'track_{track.track_id}'] = track.stopped_count

        return stats

    async def increment_users_count(self, session: AsyncSession) -> None:
        """Увеличивает количество пользователей, запустивших бота, на 1."""
        await session.execute(
            update(self.general_model).values(
                users_count=self.general_model.users_count + 1
            )
        )
        await session.commit()

    async def increment_started_count(self, session: AsyncSession):
        """Увеличивает количество начавших спектакль пользователей на 1."""
        await session.execute(
            update(self.general_model).values(
                started_count=self.general_model.started_count + 1
            )
        )
        await session.commit()

    async def increment_finished_count(self, session: AsyncSession):
        """Увеличивает количество завершивших спектакль пользователей на 1."""
        await session.execute(
            update(self.general_model).values(
                finished_count=self.general_model.finished_count + 1
            )
        )
        await session.commit()

    async def increment_track_stopped_count(self, track_id: int, session: AsyncSession):
        """Увеличивает количество дошедших до трека по его номеру на 1."""
        stmt = (
            update(self.track_model)
            .where(self.track_model.track_id == track_id)
            .values(stopped_count=self.track_model.stopped_count + 1)
        )
        await session.execute(stmt)
        await session.commit()


crud_statistics = CRUDStatistics(
    general_model=GeneralStatistics,
    track_model=TrackStatistics,
    user_model=TgUser,
)
