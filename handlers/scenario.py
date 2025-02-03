import asyncio
from pathlib import Path

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from sqlalchemy.ext.asyncio import AsyncSession

from crud.content import crud_geo, crud_sleep, crud_text, crud_track
from keyboards.reply import ScenarioKeyboard
from models.models import GeoLocation, Sleep, Text, Track
from states.states import Scenario
from utils.handler_utils import send_message_with_delay
from utils.lexicon import BUTTONS

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent
router = Router()


@router.message(F.text.in_(BUTTONS['track_1_step_1']))
async def track_1_step_1(message: Message, state: FSMContext, session: AsyncSession):
    await state.set_state(Scenario.track_1)

    track: Track = await crud_track.get_by_title('Track 1: Start', session)
    text: Text = await crud_text.get_by_title('Track 1', session)
    geo: GeoLocation = await crud_geo.get_by_title('Largo do Moinho de Vento', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_2_step_2'],
        latitude=geo.latitude,
        longitude=geo.longitude,
    )


@router.message(F.text.in_(BUTTONS['track_2_step_2']), Scenario.track_1)
async def track_2_step_2_from_saint_clara_to_church(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_2)

    track: Track = await crud_track.get_by_title(
        'Track 2: The Path from Saint Clara to the Cathedral',
        session,
    )
    text: Text = await crud_text.get_by_title('Track 2. Are you there?', session)
    sleep: Sleep = await crud_sleep.get_by_title('Track 2', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        delay=sleep.seconds,
        buttons=BUTTONS['track_2_step_3'] + BUTTONS['track_3_step_4'],
    )


@router.message(F.text.in_(BUTTONS['track_2_step_3']), Scenario.track_2)
async def track_2_step_3_help(message: Message, session: AsyncSession):
    text: Text = await crud_text.get_by_title('Track 2. Hint', session)
    geo: GeoLocation = await crud_geo.get_by_title('Largo do Moinho de Vento', session)

    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_3_step_4'],
        latitude=geo.latitude,
        longitude=geo.longitude,
    )


@router.message(F.text.in_(BUTTONS['track_3_step_4']), Scenario.track_2)
async def track_3_step_4_the_cathedral(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_3)

    track: Track = await crud_track.get_by_title('Track 3: The Cathedral', session)
    text: Text = await crud_text.get_by_title('Track 3. Keep moving', session)
    sleep: Sleep = await crud_sleep.get_by_title('Track 3', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_3_step_5'],
        delay=sleep.seconds,
    )


@router.message(F.text.in_(BUTTONS['track_3_step_5']), Scenario.track_3)
async def track_3_step_5_following_ines(message: Message, session: AsyncSession):
    text: Text = await crud_text.get_by_title('Track 3. Next path', session)
    geo: GeoLocation = await crud_geo.get_by_title('Traffic Light Route', session)

    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_3_step_6'],
        latitude=geo.latitude,
        longitude=geo.longitude,
    )


@router.message(F.text.in_(BUTTONS['track_3_step_6']), Scenario.track_3)
async def track_4_step_6_handle_the_light(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_4)

    track: Track = await crud_track.get_by_title(
        'Track 4: Heading to São Bento Station', session
    )
    text: Text = await crud_text.get_by_title(
        'Track 4. Enter São Bento Station!', session
    )
    sleep: Sleep = await crud_sleep.get_by_title('Track 4', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_4_step_7'],
        delay=sleep.seconds
    )


@router.message(F.text.in_(BUTTONS['track_4_step_7']), Scenario.track_4)
async def track_4_step_7_inside_in_the_station(message: Message, session: AsyncSession):
    text: Text = await crud_text.get_by_title('Track 4. You inside?', session)

    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_4_step_8'] + BUTTONS['track_5_step_9_base'],
    )


@router.message(F.text.in_(BUTTONS['track_4_step_8']), Scenario.track_4)
async def track_4_step_8_help(message: Message, session: AsyncSession):
    text: Text = await crud_text.get_by_title('Track 4. No worries!', session)

    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_5_step_9_help'],
    )


@router.message(
    F.text.in_(BUTTONS['track_5_step_9_base'] + BUTTONS['track_5_step_9_help']),
    Scenario.track_4
)
async def track_4_step_8_1_keep_moving(message: Message, session: AsyncSession):
    text: Text = await crud_text.get_by_title('Track 4. Keep moving', session)

    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['next'],
    )


@router.message(
    F.text.in_(BUTTONS['next']),
    Scenario.track_4,
)
async def track_5_step_9_sao_bento(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_5)

    track: Track = await crud_track.get_by_title('Track 5: São Bento Station', session)
    text_1: Text = await crud_text.get_by_title(
        'Track 5. Follow the blue cat!', session
    )
    text_2: Text = await crud_text.get_by_title('Track 5. Crossed the street?', session)
    sleep: Sleep = await crud_sleep.get_by_title('Track 5', session)
    geo: GeoLocation = await crud_geo.get_by_title('Exit São Bento Station', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text_1.content,
        latitude=geo.latitude,
        longitude=geo.longitude,
    )
    await send_message_with_delay(
        message=message,
        text=text_2.content,
        delay=sleep.seconds,
        buttons=BUTTONS['track_6_step_10'],
    )


@router.message(Scenario.track_5, F.text.in_(BUTTONS['track_6_step_10']))
async def track_6_step_10_station(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_6)

    track: Track = await crud_track.get_by_title(
        'Track 6:  Path from the Station', session
    )
    text: Text = await crud_text.get_by_title('Track 6. I absolutely love', session)
    sleep: Sleep = await crud_sleep.get_by_title('Track 6', session)
    geo: GeoLocation = await crud_geo.get_by_title('Mural', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_7_step_11'],
        delay=sleep.seconds,
        latitude=geo.latitude,
        longitude=geo.longitude,
    )


@router.message(Scenario.track_6, F.text.in_(BUTTONS['track_7_step_11']))
async def track_7_step_11_rua_das_flores(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_7)

    track: Track = await crud_track.get_by_title(
        'Track 7:  Stop at Rua das Flores – Cat Mural', session
    )
    text: Text = await crud_text.get_by_title('Track 7. Mural incredible?', session)
    geo: GeoLocation = await crud_geo.get_by_title('Lóios', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_8_step_12'],
        latitude=geo.latitude,
        longitude=geo.longitude,
    )


@router.message(Scenario.track_7, F.text.in_(BUTTONS['track_8_step_12']))
async def track_8_step_12_mural(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_8)

    track: Track = await crud_track.get_by_title(
        'Track 8:  From the Mural to Clérigos Street', session
    )
    text: Text = await crud_text.get_by_title('Track 8. In Inês’s journey', session)
    geo: GeoLocation = await crud_geo.get_by_title('Rua dos Clérigos 90 92', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_9_step_13'],
        latitude=geo.latitude,
        longitude=geo.longitude,
    )


@router.message(F.text.in_(BUTTONS['track_9_step_13']), Scenario.track_8)
async def track_9_step_13_clerigos_street(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    track: Track = await crud_track.get_by_title('Track 9.  Clérigos street', session)
    text: Text = await crud_text.get_by_title('Track 9. Next spot', session)
    geo: GeoLocation = await crud_geo.get_by_title('Clérigos street', session)
    sleep: Sleep = await crud_sleep.get_by_title('Track 9', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_10_step_14'],
        delay=sleep.seconds,
        latitude=geo.latitude,
        longitude=geo.longitude,
    )


@router.message(F.text.in_(BUTTONS['track_10_step_14']), Scenario.track_8)
async def track_9_step_13_1_special_spot(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_9)

    text: Text = await crud_text.get_by_title('Track 9. Spot is special', session)

    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['next'],
    )


@router.message(Scenario.track_9, F.text.in_(BUTTONS['next']))
async def track_10_step_14_clerigos_tower(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_10)

    track: Track = await crud_track.get_by_title('Track 10.  Clérigos tower', session)
    text: Text = await crud_text.get_by_title('Track 10. Next point', session)
    geo: GeoLocation = await crud_geo.get_by_title('Clérigos tower', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_11_step_15'],
        latitude=geo.latitude,
        longitude=geo.longitude,
    )


@router.message(Scenario.track_10, F.text.in_(BUTTONS['track_11_step_15']))
async def track_11_step_15_teixeia_square(
        message: Message, state: FSMContext, session: AsyncSession
):
    await state.set_state(Scenario.track_11)

    track: Track = await crud_track.get_by_title(
        'Track 11. From Clérigos Tower to Teixeira Square', session
    )
    text: Text = await crud_text.get_by_title('Track 11. Fountain beautiful', session)
    sleep: Sleep = await crud_sleep.get_by_title('Track 11', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_12_step_16'],
        delay=sleep.seconds,
    )


@router.message(Scenario.track_11, F.text.in_(BUTTONS['track_12_step_16']))
async def track_12_step_16_meeting_rita(
        message: Message, state: FSMContext, session: AsyncSession
):
    await state.set_state(Scenario.track_12)

    track: Track = await crud_track.get_by_title(
        'Track 12: Teixeira Square – Meeting Rita', session
    )
    sleep: Sleep = await crud_sleep.get_by_title('Track 12', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text='Can you see the note?',
        buttons=BUTTONS['track_12_step_17'],
        delay=sleep.seconds,
    )


@router.message(Scenario.track_12, F.text.in_(BUTTONS['track_12_step_17']))
async def track_12_step_17_note(
        message: Message, state: FSMContext, session: AsyncSession
):
    track: Track = await crud_track.get_by_title(
        'Track 12: Teixeira Square – Meeting Rita', session
    )
    text: Text = await crud_text.get_by_title('Track 12. Curious to find', session)

    await message.answer_animation(
        FSInputFile(track.animation)
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_13_step_18'],
    )


@router.message(Scenario.track_12, F.text.in_(BUTTONS['track_13_step_18']))
async def track_12_step_17_1_next_stop(
        message: Message, state: FSMContext, session: AsyncSession
):
    text: Text = await crud_text.get_by_title('Track 12. Traffic light safely', session)
    geo: GeoLocation = await crud_geo.get_by_title(
        'Praça de Carlos Alberto 131', session
    )

    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['next'],
        latitude=geo.latitude,
        longitude=geo.longitude,
    )


@router.message(Scenario.track_12, F.text.in_(BUTTONS['next']))
async def track_13_step_18_carlos_alberto_square(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_13)

    track: Track = await crud_track.get_by_title(
        'Track 13: From Teixeira Square to Carlos Alberto Square', session
    )
    text: Text = await crud_text.get_by_title('Track 13. Next destination', session)
    geo: GeoLocation = await crud_geo.get_by_title('From Teixeira Square', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_14_step_19'],
        latitude=geo.latitude,
        longitude=geo.longitude,
    )


@router.message(Scenario.track_13, F.text.in_(BUTTONS['track_14_step_19']))
async def track_14_step_19_meeting_carolina(
        message: Message, state: FSMContext, session: AsyncSession
):
    await state.set_state(Scenario.track_14)

    track: Track = await crud_track.get_by_title(
        'Track 14: Carlos Alberto Square – Meeting Carolina', session
    )
    sleep: Sleep = await crud_sleep.get_by_title('Track 14', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await asyncio.sleep(
        sleep.seconds
    )
    await message.answer_animation(
        message=message,
        animation=FSInputFile(track.animation),
        reply_markup=ScenarioKeyboard(BUTTONS['track_15_step_20']).get_keyboard(),
    )


@router.message(Scenario.track_14, F.text.in_(BUTTONS['track_15_step_20']))
async def track_15_step_20_carolina(
        message: Message, state: FSMContext, session: AsyncSession
):
    await state.set_state(Scenario.track_15)

    track: Track = await crud_track.get_by_title(
        'Track 15: Carlos Alberto Square – Carolina', session
    )
    text: Text = await crud_text.get_by_title('Track 15. Torn piece', session)
    sleep: Sleep = await crud_sleep.get_by_title('Track 15', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_15_step_21'],
        delay=sleep.seconds,
    )


@router.message(Scenario.track_15, F.text.in_(BUTTONS['track_15_step_21']))
async def track_15_step_21_page(message: Message, session: AsyncSession):
    track: Track = await crud_track.get_by_title(
        'Track 15: Carlos Alberto Square – Carolina', session
    )

    await message.answer_animation(
        FSInputFile(track.animation),
        reply_markup=ScenarioKeyboard(BUTTONS['track_16_step_22']).get_keyboard(),
    )


@router.message(Scenario.track_15, F.text.in_(BUTTONS['track_16_step_22']))
async def track_16_step_22_carolina_finale(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_16)

    track: Track = await crud_track.get_by_title(
        'Track 16: Carlos Alberto Square – Carolina’s Finale', session
    )
    text_1: Text = await crud_text.get_by_title(
        'Track 16. Largo do Moinho de Vento', session
    )
    text_2: Text = await crud_text.get_by_title('Track 16. Beautiful azulejo', session)
    sleep: Sleep = await crud_sleep.get_by_title('Track 16', session)
    geo: GeoLocation = await crud_geo.get_by_title('Carlos Alberto Square', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text_1.content,
        latitude=geo.latitude,
        longitude=geo.longitude,
    )
    await send_message_with_delay(
        message=message,
        text=text_2.content,
        buttons=BUTTONS['track_17_step_23'],
        delay=sleep.seconds,
    )


@router.message(F.text.in_(BUTTONS['track_17_step_23']), Scenario.track_16)
async def track_17_step_23_azulejo(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_17)

    track: Track = await crud_track.get_by_title(
        'Track 17: Largo do Moinho de Vento – The Azulejo', session
    )
    text: Text = await crud_text.get_by_title('Track 17. Joana Vasconcelos', session)
    sleep_1: Sleep = await crud_sleep.get_by_title('Track 17_1', session)
    sleep_2: Sleep = await crud_sleep.get_by_title('Track 17_2', session)
    geo: GeoLocation = await crud_geo.get_by_title('R. de Ceuta 33', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        delay=sleep_1.seconds,
        latitude=geo.latitude,
        longitude=geo.longitude,
    )
    await send_message_with_delay(
        message=message,
        text='Are you ready to continue?',
        delay=sleep_2.seconds,
        buttons=BUTTONS['track_18_step_24']
    )


@router.message(F.text.in_(BUTTONS['track_18_step_24']), Scenario.track_17)
async def track_18_step_24_cafe_ceuta(
        message: Message, state: FSMContext, session: AsyncSession
):
    track: Track = await crud_track.get_by_title('Track 18: Café Ceuta', session)
    text: Text = await crud_text.get_by_title('Track 18. Laurinda and Aurélia', session)
    sleep: Sleep = await crud_sleep.get_by_title('Track 18_1', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await asyncio.sleep(
        sleep.seconds
    )
    await message.answer_animation(
        animation=FSInputFile(track.animation),
    )
    await send_message_with_delay(
        message=message,
        text=text.content,
        buttons=BUTTONS['track_19_step_25'],
    )


@router.message(F.text.in_(BUTTONS['track_19_step_25']), Scenario.track_17)
async def track_18_step_24_1_next_stop(
        message: Message, state: FSMContext, session: AsyncSession
):
    await state.set_state(Scenario.track_18)

    text: Text = await crud_text.get_by_title('Track 18. Next stop', session)
    geo: GeoLocation = await crud_geo.get_by_title(
        'Entry Hotel Infante Sagres', session
    )

    await send_message_with_delay(
        message=message,
        text=text.content,
        latitude=geo.latitude,
        longitude=geo.longitude,
        buttons=BUTTONS['next'],
    )


@router.message(F.text.in_(BUTTONS['next']), Scenario.track_18)
async def track_19_step_25_hotel_infante_sagres(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(Scenario.track_19)

    track: Track = await crud_track.get_by_title(
        'Track 19: Hotel Infante Sagres', session
    )
    text_1: Text = await crud_text.get_by_title('Track 19. Inês is starting', session)
    text_2: Text = await crud_text.get_by_title(
        'Track 19. Beautiful buildings', session
    )
    sleep_1: Sleep = await crud_sleep.get_by_title('Track 19_1', session)
    sleep_2: Sleep = await crud_sleep.get_by_title('Track 19_2', session)
    geo: GeoLocation = await crud_geo.get_by_title('Avenida dos Aliados', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text_1.content,
        delay=sleep_1.seconds,
        latitude=geo.latitude,
        longitude=geo.longitude,
    )
    await send_message_with_delay(
        message=message,
        text=text_2.content,
        buttons=BUTTONS['track_20_step_26'],
        delay=sleep_2.seconds,
    )


@router.message(F.text.in_(BUTTONS['track_20_step_26']), Scenario.track_19)
async def track_20_step_26_city_hall(
        message: Message, state: FSMContext, session: AsyncSession
):
    await state.set_state(Scenario.track_20)

    track: Track = await crud_track.get_by_title('Track 20: City Hall', session)
    text_1: Text = await crud_text.get_by_title('Track 20. Cristina', session)
    text_2: Text = await crud_text.get_by_title('Track 20. Remember Cristina', session)
    sleep: Sleep = await crud_sleep.get_by_title('Track 20', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text_1.content,
        delay=sleep.seconds
    )
    await message.answer_animation(
        FSInputFile(track.animation)
    )
    await send_message_with_delay(
        message=message,
        text=text_2.content,
        buttons=BUTTONS['track_21_step_27'],
    )


@router.message(F.text.in_(BUTTONS['track_21_step_27']), Scenario.track_20)
async def track_21_step_27_abbess(
        message: Message, state: FSMContext, session: AsyncSession
):
    await state.set_state(Scenario.track_21)

    track: Track = await crud_track.get_by_title(
        'Track 21: Meeting the Abbess – The Finale', session
    )
    text_1: Text = await crud_text.get_by_title('Track 21. Inês', session)
    text_2: Text = await crud_text.get_by_title('Track 21. Thank you', session)
    sleep_1: Sleep = await crud_sleep.get_by_title('Track 21_1', session)
    sleep_2: Sleep = await crud_sleep.get_by_title('Track 21_2', session)

    await message.answer_audio(
        audio=FSInputFile(track.audio),
        title=track.title,
    )
    await send_message_with_delay(
        message=message,
        text=text_1.content,
        delay=sleep_1.seconds,
    )
    await send_message_with_delay(
        message=message,
        text=text_2.content,
        delay=sleep_2.seconds,
        buttons=BUTTONS['track_21_step_28'] + BUTTONS['track_21_step_29'],
    )


@router.message(F.text.in_(BUTTONS['track_21_step_28']), Scenario.track_21)
async def track_21_step_28_like(message: Message, session: AsyncSession):
    text: Text = await crud_text.get_by_title('Track 21. That is wonderful', session)

    await send_message_with_delay(
        message=message,
        text=text.content,
    )


@router.message(F.text.in_(BUTTONS['track_21_step_29']), Scenario.track_21)
async def track_21_step_29_dislike(message: Message, session: AsyncSession):
    text: Text = await crud_text.get_by_title('Track 21. Sorry to hear', session)

    await send_message_with_delay(
        message=message,
        text=text.content,
    )
