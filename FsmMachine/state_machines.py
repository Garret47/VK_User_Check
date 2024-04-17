from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class VkSearchMachine(StatesGroup):
    NumberChoice = State()
    SearchModeChoice = State()
    LoadFile = State()
