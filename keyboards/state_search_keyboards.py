from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

inline_buttons = [[InlineKeyboardButton(text='Только сообщества', callback_data='communities')],
                          [InlineKeyboardButton(text='Только пользователи', callback_data='people')],
                          [InlineKeyboardButton(text='И пользователи, и сообщества', callback_data='all')]]

kb_inline_state_search = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
