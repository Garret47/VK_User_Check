from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from assist_func import json_methods

FileNameStateSearch = './data/keyboard_text.json'
text_keyboards = json_methods.read_file_json(FileNameStateSearch)

inline_buttons = [[InlineKeyboardButton(text=text_keyboards['communities'], callback_data='communities')],
                  [InlineKeyboardButton(text=text_keyboards['people'], callback_data='people')],
                  [InlineKeyboardButton(text=text_keyboards['all'], callback_data='all')]]

buttons = [[KeyboardButton(text=text_keyboards['cancel_state'])]]

kb_inline_state_search = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
kb_reply_state_search = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
