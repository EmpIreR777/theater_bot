import os

from fastapi.requests import Request
from itsdangerous.exc import BadSignature
from itsdangerous.serializer import Serializer
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from wtforms import TextAreaField

from crud.users import crud_user
from db.engine import async_session_maker
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


class AdminAuth(AuthenticationBackend):
    """
    Класс для управления аутентификацией администратора.

    Args:
        secret_key (str): Секретный ключ для сериализации токенов.

    """

    def __init__(self, secret_key: str):
        super().__init__(secret_key)
        self.serializer = Serializer(secret_key)

    async def login(self, request: Request) -> bool:
        """
        Обрабатывает вход администратора.

        Args:
            request (Request): Запрос с формой, содержащей username и password.

        Returns:
            bool: True, если пользователь успешно аутентифицирован, иначе False.

        """
        form = await request.form()
        username, password = form['username'], form['password']

        async with async_session_maker() as session:
            admin = await crud_user.get_user(
                username=username,
                password=password,
                session=session,
            )

        if admin:
            data = username + password
            token = self.serializer.dumps(data)
            request.session.update({'token': token})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        """
        Выполняет выход администратора.

        Args:
            request (Request): Запрос сессии.

        Returns:
            bool: True после очистки сессии.

        """
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """
        Проверяет подлинность токена администратора.

        Args:
            request (Request): Запрос сессии.

        """
        token = request.session.get('token')

        if not token:
            return False

        try:
            self.serializer.loads(token)
            return True

        except BadSignature:
            return False


class TrackAdmin(ModelView, model=Track):
    """Админ-панель для управления треками."""

    name = 'Трек'
    name_plural = 'Треки'
    icon = 'fas fa-route'
    column_list = [
        'number',
        'title',
        'audio',
        'photo',
        'animation',
        'texts',
        'locations',
        'sleeps',
        'statistics',
    ]
    column_labels = {
        'number': 'Номер',
        'title': 'Название',
        'audio': 'Аудио',
        'photo': 'Фото',
        'animation': 'Анимация',
        'texts': 'Тексты',
        'locations': 'Локации',
        'sleeps': 'Паузы',
        'statistics': 'Статистика',
    }
    column_details_list = column_list

    column_searchable_list = ['title']
    column_sortable_list = ['number', 'title']
    page_size = 20

    column_formatters = {
        Track.audio: lambda m, _: os.path.split(m.audio)[1] if m.audio else '',
        Track.photo: lambda m, _: os.path.split(m.photo)[1] if m.photo else '',
        Track.animation: lambda m, _: os.path.split(m.animation)[1]
        if m.animation
        else '',
    }

    form_create_rules = [
        'number',
        'title',
        'audio',
        'photo',
        'animation',
    ]

    # form_edit_rules = ['audio', 'photo', 'animation']

    # can_create = False
    # can_edit = True
    # can_delete = False

    # form_columns = ['sleep_seconds', 'track_sound', 'photo']
    # column_details_list = '__all__'  # Не разобрался
    # Настройка асинхронной загрузки для поля user_id
    # form_ajax_refs = {
    #     'track_text': {
    #         'fields': ['text_content'],  # Поля, по которым будет осуществляться поиск
    #         'order_by': ['text_content'],  # Опционально: сортировка
    #         'page_size': 22,  # Количество записей на одну загрузку
    #     }
    # }


class TextAdmin(ModelView, model=Text):
    """Админ-панель для управления текстами треков."""

    name = 'Текст'
    name_plural = 'Тексты'
    icon = 'fa fa-text-width'

    column_list = ['track', 'title']
    column_labels = {
        'track': 'Трек',
        'title': 'Заголовок текста',
        'content': 'Текст',
    }
    column_searchable_list = ['title']
    column_sortable_list = ['title']

    form_overrides = {'content': TextAreaField}
    form_widget_args = {'content': {'rows': 10}}

    # form_edit_rules = ['content']

    # can_create = False
    # can_edit = True
    # can_delete = False


class GeoLocationAdmin(ModelView, model=GeoLocation):
    """Админ-панель для управления геолокациями треков."""

    name = 'Локация'
    name_plural = 'Локации'
    icon = 'fa-solid fa-location-crosshairs'

    column_list = ['track', 'title', 'geo_link', 'latitude', 'longitude']
    column_labels = {
        'track': 'Трек',
        'title': 'Название',
        'geo_link': 'Ссылка',
        'latitude': 'Широта',
        'longitude': 'Долгота',
    }
    column_searchable_list = ['title', 'geo_link']
    column_sortable_list = ['title', 'latitude', 'longitude']

    # form_edit_rules = ['geo_link', 'latitude', 'longitude']

    # can_create = False
    # can_edit = True
    # can_delete = False


class SleepAdmin(ModelView, model=Sleep):
    """Админ-панель для управления паузами."""

    name = 'Пауза'
    name_plural = 'Паузы'
    icon = 'fa-solid fa-stopwatch'

    column_list = ['track', 'title', 'seconds']
    column_labels = {
        'track': 'Трек',
        'title': 'Название',
        'seconds': 'Длительность (сек)',
    }
    column_searchable_list = ['title']
    column_sortable_list = ['title', 'seconds']

    # form_edit_rules = ['seconds']

    # can_create = False
    # can_edit = True
    # can_delete = False


class TgUserAdmin(ModelView, model=TgUser):
    """Админ-панель для управления пользователями Telegram."""

    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'

    column_list = [
        'tg_user_id',
        'username',
        'first_name',
        'last_name',
        'authorized',
        'can_see_statistics',
        'last_active',
    ]
    column_labels = {
        'tg_user_id': 'ID в Telegram',
        'username': 'Ник',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'authorized': 'Авторизация',
        'can_see_statistics': 'Доступ к статистике',
        'last_active': 'Последняя активность',
    }

    column_filters = [
        'tg_user_id',
        'username',
        'first_name',
        'last_name',
        'can_see_statistics',
    ]
    column_searchable_list = [
        'username',
        'first_name',
        'last_name',
    ]
    column_sortable_list = ['tg_user_id', 'last_active', 'can_see_statistics']

    # can_create = False
    # can_edit = True
    # can_delete = True


class UserAdmin(ModelView, model=User):
    """Админ-панель для управления администраторами."""

    name = 'Администратор'
    name_plural = 'Администраторы'
    icon = 'fa-solid fa-clipboard-user'

    column_list = ['username']
    column_labels = {
        'username': 'Логин',
        'password': 'Пароль',
    }
    column_searchable_list = ['username']
    column_sortable_list = ['username']

    # can_create = True
    # can_edit = True
    # can_delete = True


class GeneralStatisticsAdmin(ModelView, model=GeneralStatistics):
    """Общая статистика спектакля."""

    name = 'Общая статистика'
    name_plural = 'Общая статистика'
    icon = 'fa-solid fa-chart-line'

    column_list = ['users_count', 'started_count', 'finished_count']
    column_labels = {
        'users_count': 'Количество пользователей',
        'started_count': 'Начали спектакль',
        'finished_count': 'Закончили спектакль',
    }

    # can_create = False
    # can_edit = False
    # can_delete = False


class TrackStatisticsAdmin(ModelView, model=TrackStatistics):
    """Статистика по трекам."""

    name = 'Статистика по треку'
    name_plural = 'Статистика по трекам'
    icon = 'fa-solid fa-person-walking-dashed-line-arrow-right'

    column_list = ['track', 'stopped_count']
    column_labels = {
        'track': 'Трек',
        'stopped_count': 'Кол-во остановившихся',
    }

    column_sortable_list = ['track_id', 'stopped_count']

    # can_create = False
    # can_edit = False
    # can_delete = False


class CouponAdmin(ModelView, model=Coupon):
    """Промокоды."""

    name = 'Купон'
    name_plural = 'Купоны'
    icon = 'fa-solid fa-ticket'

    column_list = ['code', 'is_active']
    column_labels = {
        'code': 'Код',
        'is_active': 'Активен?',
    }

    column_filters = ['code', 'is_active']
    column_searchable_list = ['code']
    column_sortable_list = ['code']
