from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class VkSettingMachine(StatesGroup):
    NumberChoice = State()
    SettingModeChoice = State()
    Communities = State()
    People = State()
    All = State()
