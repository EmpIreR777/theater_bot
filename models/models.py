from datetime import datetime

from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import config
from db.database import Base


class TgUser(Base):
    """Телеграм-пользователь"""

    tg_user_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(nullable=True, default='')
    first_name: Mapped[str] = mapped_column(nullable=True, default='')
    last_name: Mapped[str] = mapped_column(nullable=True, default='')
    authorized: Mapped[bool] = mapped_column(default=False)
    last_active: Mapped[datetime] = mapped_column(default=datetime.now())
    can_see_statistics: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f'id: {self.tg_user_id}, username: {self.username or "<отсутствует>"}'


class User(Base):
    """Пользователь админ-панели"""

    username: Mapped[str] = mapped_column(
        String(length=255),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)

    def __str__(self):
        return self.username


class Coupon(Base):
    """Промокод"""

    code: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    def __repr__(self) -> str:
        return f"{self.code}: {'активен' if self.is_active else 'деактивирован'}"


class Track(Base):
    """Трек"""

    number: Mapped[int] = mapped_column(unique=True, nullable=False)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)

    audio: Mapped[FileType | None] = mapped_column(
        FileType(storage=config.STORAGES['audio']),
        default='',
        nullable=True,
    )
    photo: Mapped[FileType | None] = mapped_column(
        FileType(storage=config.STORAGES['image']),
        default='',
        nullable=True,
    )
    animation: Mapped[FileType | None] = mapped_column(
        FileType(storage=config.STORAGES['animation']),
        default='',
        nullable=True,
    )

    texts: Mapped[list['Text']] = relationship(
        'Text',
        back_populates='track',
        cascade='all, delete-orphan',
    )

    locations: Mapped[list['GeoLocation']] = relationship(
        'GeoLocation',
        back_populates='track',
        cascade='all, delete-orphan',
    )

    sleeps: Mapped[list['Sleep']] = relationship(
        'Sleep',
        back_populates='track',
        cascade='all, delete-orphan',
    )

    statistics: Mapped['TrackStatistics'] = relationship(
        'TrackStatistics',
        back_populates='track',
        cascade='all, delete-orphan',
        uselist=False,
    )

    def __repr__(self):
        return self.title


class Text(Base):
    """Текст"""

    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'), nullable=False)

    track: Mapped['Track'] = relationship(
        'Track',
        back_populates='texts',
        lazy='joined',
    )

    def __repr__(self):
        return self.title


class GeoLocation(Base):
    """Геолокация"""

    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    geo_link: Mapped[str] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'), nullable=False)

    track: Mapped['Track'] = relationship('Track', back_populates='locations')

    def __repr__(self):
        return self.title


class Sleep(Base):
    """Пауза"""

    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'), nullable=False)
    seconds: Mapped[float] = mapped_column(nullable=False, default=0.1)

    track: Mapped['Track'] = relationship('Track', back_populates='sleeps')

    def __repr__(self):
        return self.title


class GeneralStatistics(Base):
    """Общая статистика по спектаклю"""

    users_count: Mapped[int] = mapped_column(default=0)
    started_count: Mapped[int] = mapped_column(default=0)
    finished_count: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f'Спектакль начат {self.started_count} раз, завершен {self.finished_count} раз'


class TrackStatistics(Base):
    """Статистика по трекам"""

    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'), nullable=False)
    stopped_count: Mapped[int] = mapped_column(default=0)

    track: Mapped['Track'] = relationship('Track', back_populates='statistics')

    def __repr__(self):
        return f'Трек №{self.track_id}, количество переходов: {self.stopped_count}'
