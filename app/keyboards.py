from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

from config import CHANNEL_URL


main_kb = InlineKeyboardMarkup(inline_keyboard= [
    [
        InlineKeyboardButton(text='Подписаться', url=f'{CHANNEL_URL}')
    ],
    [
        InlineKeyboardButton(text='Проверить', callback_data='sub_check')
    ]
])



#################### admin buttons ####################

async def admin_menu():
    keyboard = ReplyKeyboardBuilder()
    
    keyboard.row(
    KeyboardButton(text='Добавить'),
    KeyboardButton(text='Посмотреть пост'),
    KeyboardButton(text='Выход')
    ), 
    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)

#################### admin buttons ####################