import asyncio
import logging
from datetime import datetime

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI
from sqladmin import Admin

from admin.admin_panel import (
    AdminAuth,
    CouponAdmin,
    GeneralStatisticsAdmin,
    GeoLocationAdmin,
    SleepAdmin,
    TextAdmin,
    TgUserAdmin,
    TrackAdmin,
    TrackStatisticsAdmin,
    UserAdmin,
)
from config import config
from db.engine import async_session_maker, engine
from handlers import introduction, scenario
from middlewares.middleware import DataBaseSession

app = FastAPI()
authentication_backend = AdminAuth(secret_key=config.SECRET_KEY)

admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
)


logging.basicConfig(level=logging.INFO)

admin.add_view(TrackAdmin)
admin.add_view(TextAdmin)
admin.add_view(GeoLocationAdmin)
admin.add_view(SleepAdmin)
admin.add_view(TgUserAdmin)
admin.add_view(UserAdmin)
admin.add_view(GeneralStatisticsAdmin)
admin.add_view(TrackStatisticsAdmin)
admin.add_view(CouponAdmin)


async def start_aiogram():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(bot=bot)
    dp.update.middleware(DataBaseSession(async_session=async_session_maker))
    dp['started_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    dp.include_router(introduction.router)
    dp.include_router(scenario.router)

    await dp.start_polling(bot)


async def start_fastapi():
    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(start_aiogram(), start_fastapi())


if __name__ == '__main__':
    asyncio.run(main())
