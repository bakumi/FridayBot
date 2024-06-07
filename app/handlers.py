from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import CHANNEL_ID
import app.keyboards as kb
import app.admin as admin



router = Router()



@router.message(CommandStart())
async def command_start(message: Message, bot):
    sub = await bot.get_chat_member(CHANNEL_ID, user_id=message.from_user.id)

    if sub.status != 'left':
        await message.answer('Добро пожаловать!')
        await send_saved_post(message, bot)
    else:
        await message.answer('Подпишись, чтобы пользоваться ботом', reply_markup=kb.main_kb)



@router.callback_query(F.data == 'sub_check')
async def sub(callback: CallbackQuery, bot):
    sub = await bot.get_chat_member(CHANNEL_ID, user_id=callback.from_user.id)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    if sub.status != 'left':
        await callback.message.answer('Добро пожаловать!')
        await send_saved_post(callback.message, bot)
    else:
        await callback.message.answer('Подпишитесь, чтобы пользоваться ботом', reply_markup=kb.main_kb)



async def send_saved_post(message: Message, bot):
    data = admin.get_saved_post_data()
    if data:
        inline_markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=data[3], callback_data='button_1')],
            [InlineKeyboardButton(text=data[4], callback_data='button_2')],
            [InlineKeyboardButton(text=data[5], callback_data='button_3')]
        ])
        await bot.send_photo(chat_id=message.chat.id, photo=data[0], caption=data[1], reply_markup=inline_markup)
    else:
        await message.answer('Нет доступных постов для просмотра.')



@router.message(F.text.lower() == 'посмотреть пост')
async def view_post(message: Message, bot):
    data = admin.get_saved_post_data()
    if data:
        inline_markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=data[3], callback_data='button_1')],
            [InlineKeyboardButton(text=data[4], callback_data='button_2')],
            [InlineKeyboardButton(text=data[5], callback_data='button_3')]
        ])
        await bot.send_photo(chat_id=message.chat.id, photo=data[0], caption=data[1], reply_markup=inline_markup)
    else:
        await message.answer('Нет доступных постов для просмотра.')
