from aiogram.utils.keyboard import (
    KeyboardButton,
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
)

from utils.lexicon import MAIN_MENU


class ReplyBuilder:
    def __init__(self):
        self.keyboard = ReplyKeyboardBuilder()

    def add_buttons(self, buttons: list[str] | tuple[str]) -> None:
        for button in buttons:
            self.keyboard.add(KeyboardButton(text=button))

    def get_keyboard(
        self,
        row: int = 1,
        is_one_time: bool = True,
    ) -> ReplyKeyboardMarkup:
        return self.keyboard.adjust(row).as_markup(
            resize_keyboard=True,
            input_field_placeholder='Use the menu:',
            one_time_keyboard=is_one_time,
        )


class MainKeyboard(ReplyBuilder):
    def __init__(self):
        super().__init__()
        self.add_buttons(MAIN_MENU.keys())

    def get_keyboard(self):
        return super().get_keyboard(row=2, is_one_time=False)


class ScenarioKeyboard(ReplyBuilder):
    def __init__(self, specific_buttons: list[str]):
        super().__init__()
        self.add_buttons(specific_buttons)
