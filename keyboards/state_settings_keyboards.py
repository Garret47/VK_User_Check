from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from assist_func import json_methods

FileNameStateSettings = './data/keyboard_text.json'
text_keyboards = json_methods.read_file_json(FileNameStateSettings)

inline_buttons_mode = [[InlineKeyboardButton(text=text_keyboards['communities'], callback_data='communities')],
                       [InlineKeyboardButton(text=text_keyboards['people'], callback_data='people')],
                       [InlineKeyboardButton(text=text_keyboards['all'], callback_data='all')]]

buttons = [[KeyboardButton(text=text_keyboards['cancel_state'])]]

kb_inline_state_mode = InlineKeyboardMarkup(inline_keyboard=inline_buttons_mode)
kb_inline_state_setting_value = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=text_keyboards["default_value"], callback_data='default')]])
kb_reply_state_setting = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
