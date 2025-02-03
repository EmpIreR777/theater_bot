from pathlib import Path

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from crud.base import crud_tg_user
from crud.content import crud_geo
from crud.coupons import crud_coupons
from crud.statistics import crud_statistics
from db.engine import async_session_maker
from keyboards.reply import MainKeyboard, ScenarioKeyboard
from main import logging
from states.states import Scenario
from utils.handler_utils import send_message_with_delay
from utils.lexicon import BUTTONS, MAIN_MENU, TEXT
from utils.utils import format_statistics_message

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    await crud_statistics.increment_users_count(session)
    await state.set_state(Scenario.coupons)
    await message.answer(
        text=TEXT['enter_code']
    )


@router.message(Scenario.coupons)
async def handle_coupons(message: Message, state: FSMContext, session: AsyncSession):
    text = message.text.strip()
    coupon = await crud_coupons.get_by_code(text, session)

    if coupon:
        await state.set_state(Scenario.user)
        await crud_coupons.deactivate(text, session)
        await message.answer(
            text=TEXT['great'],
            reply_markup=ScenarioKeyboard(BUTTONS['🔵 Let’s Begin']).get_keyboard(),
        )

    else:
        await message.answer(text=TEXT['not_code'])


@router.message(Scenario.user)
async def handle_user(message: Message, state: FSMContext, session: AsyncSession):
    user = await crud_tg_user.get_by_attribute(
        'tg_user_id',
        message.from_user.id,
        session,
    )
    try:
        if not user:
            obj_in = {
                'tg_user_id': message.from_user.id,
                'first_name': message.from_user.first_name,
                'username': message.from_user.username,
            }
            await crud_statistics.create(obj_in, session)
    except Exception as e:
        logging.error(f'Ошибка при добавлении пользователя: {e!s}')
    await state.set_state(Scenario.introduction)
    await message.answer(
        text=TEXT['start_text'],
        reply_markup=MainKeyboard().get_keyboard(),
    )


@router.message(F.text.in_(MAIN_MENU.keys()), Scenario.introduction)
async def handle_instructions(message: Message, session: AsyncSession):
    if message.text == "Let's begin":
        await message.answer(
            text=MAIN_MENU["Let's begin"],
            reply_markup=ScenarioKeyboard(BUTTONS['proof_location']).get_keyboard(),
        )

        # geo = await crud_geo.get_lat_long(1, session)  # НЕ СТАЛ РАЗБИРАТЬСЯ с track_id поставил заглушку (1)
        geo = await crud_geo.get_by_attribute(
            attr_name='track_id',
            attr_value=1,
            session=session,
        )
        await message.bot.send_location(
            chat_id=message.chat.id,
            latitude=geo.latitude,
            longitude=geo.longitude,
        )
    else:
        await message.answer(text=MAIN_MENU[message.text])


@router.message(F.text.in_(BUTTONS['proof_location']), Scenario.introduction)
async def handle_attention(message: Message):
    await send_message_with_delay(
        message=message,
        text=TEXT['disclaimer_text'],
        buttons=BUTTONS['track_1_step_1'],
    )


@router.message(F.text == 'statistic', F.from_user.id.in_(config.ADMIN_IDS))
async def admin_statistic(
    message: Message,
    state: FSMContext,
):
    """
    Обработчик  запроса для получения статистики.
    Собирает и отображает статистику по пользователям и заявкам.
    """
    try:
        await message.answer('📊 Собираем статистику...')
        async with async_session_maker() as session:
            stats_people = await crud_statistics.get_user_statistics(session=session)
            scenario_stats = await crud_statistics.get_scenario_statistics(
                session=session
            )
        # надо дописать функцию format_statistics_message
        # ей передается словарь со статистикой по сценарию и трекама
        # нужно добавить это в вывод
        user_stats_message = format_statistics_message(stats_people, scenario_stats)
        await send_message_with_delay(
            message=message,
            text=user_stats_message,
            reply_markup=MainKeyboard().get_keyboard(),
        )

    except Exception as e:
        error_msg = f'Ошибка при сборе статистики: {e!s}'
        logging.error(error_msg, exc_info=True)
        await message.answer(
            '❌ Произошла ошибка при сборе статистики. Попробуйте позже.',
        )
