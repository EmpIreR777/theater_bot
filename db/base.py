"""Импорты класса Base и всех моделей для Alembic."""

from db.database import Base
from models.models import (
    Coupon,
    GeneralStatistics,
    GeoLocation,
    Sleep,
    Text,
    TgUser,
    Track,
    TrackStatistics,
    User,
)

__all__ = [
    'Base',
    'Coupon',
    'GeneralStatistics',
    'GeoLocation',
    'Sleep',
    'Text',
    'TgUser',
    'Track',
    'TrackStatistics',
    'User',
]
