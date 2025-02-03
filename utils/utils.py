from datetime import datetime

from aiogram.types import CallbackQuery


def get_user_data(callback: CallbackQuery) -> dict:
    return {
        'tg_user_id': callback.from_user.id,
        'username': callback.from_user.username,
        'first_name': callback.from_user.first_name,
        'last_name': callback.from_user.last_name,
    }


def format_statistics_message(stats_people, stats_scenario) -> str:
    """Форматирует сообщение со статистикой."""
    current_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    return (
        '📈 Статистика пользователей и заявок:\n\n'
        f'👥 Всего пользователей: {stats_people["total_users"]}\n\n'
        f'🆕 Людей за сегодня: {stats_people["new_today"]}\n'
        f'📅 Людей за неделю: {stats_people["new_week"]}\n'
        f'📆 Людей за месяц: {stats_people["new_month"]}\n\n'
        f'🕒 Данные актуальны на: {current_time}'
    )


# async def add_buttons_to_db(track_id, session):
#
#     for button_key, buttons in BUTTONS.items():
#         if button_key.startswith(f'track_{track_id}'):
#             for button_text in buttons:
#                 button_data = {
#                     'button_text': button_text,
#                     'track_id': track_id
#                 }
#                 await crud_button.create(button_data, session)
#
#
# async def add_texts_to_db(track_id, session):
#     for text_key, text_content in TEXT.items():
#         if text_key.startswith(f'track_{track_id}'):
#             if isinstance(text_content, list):
#                 for content in text_content:
#                     text_data = {
#                         'text_content': content,
#                         'track_id': track_id
#                     }
#                     await crud_text.create(text_data, session)
#             else:
#                 text_data = {
#                     'text_content': text_content,
#                     'track_id': track_id
#                 }
#                 await crud_text.create(text_data, session)
#
#
# async def add_tracks_to_db(session):
#
#     for key in TRACK_TITLE:
#         track_data = {
#             'track_number': int(key.split('_')[1]),
#             'track_name': TRACK_TITLE[key],
#             'track_sound': TRACK_URL[key],
#             'photo': PICTURE_URL.get(key, None),
#             'video': ANIMATION_URL.get(key, None),
#         }
#         track = await crud_track.create(track_data, session)
#         await add_buttons_to_db(track.id, session)
#         await add_texts_to_db(track.id, session)
#         await import_location(track.id, session)
#
#
# async def import_location(track_id, session):
#     if track_id in LOCATION:
#         coordinates = LOCATION[track_id]
#         if coordinates:
#             if isinstance(coordinates[0], list):
#                 for lat_long in coordinates:
#                     geo_data = {
#                         'name': f'{track_id}',
#                         'geo_link': '',
#                         'latitude': lat_long[0],
#                         'longitude': lat_long[1],
#                         'track_id': track_id
#                     }
#                     await crud_geo.create(geo_data, session)
#             else:
#                 geo_data = {
#                     'name': f'{track_id}',
#                     'geo_link': '',
#                     'latitude': coordinates[0],
#                     'longitude': coordinates[1],
#                     'track_id': track_id
#                 }
#                 await crud_geo.create(geo_data, session)
#
#
# async def init_geo(session):
#     for track_id in LOCATION.keys():
#         await import_location(track_id, session)
