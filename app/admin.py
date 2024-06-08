from aiogram import Router, F
from datetime import datetime, timedelta
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command, Filter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from app.database import AddInfo, admin_db, save_post_data, get_saved_post_data, user_db
from config import ADMIN_ID
import app.keyboards as kb



admin = Router()



#################### admin protect ####################

class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id == ADMIN_ID

#################### admin protect ####################



#################### open admin menu ####################

@admin.message(AdminProtect(), Command('admin'))
async def adminPanel(message: Message):
    await message.answer(f'Вы вошли в админ панель.\n\nПользователь: {message.from_user.full_name}\nId: {message.from_user.id}\nUsername: @{message.from_user.username}', reply_markup=await kb.admin_menu())

#################### open admin menu ####################



#################### exit from admin menu ####################

@admin.message(AdminProtect(), F.text.lower() == 'выход')
async def exit_pan(message: Message, bot):
    await bot.send_message(chat_id=message.from_user.id, text="Админ панель закрыта", reply_markup=ReplyKeyboardRemove())

#################### exit from admin menu ####################



#################### create post ####################

@admin.message(AdminProtect(), StateFilter(None), F.text.lower() == 'добавить')
async def add_photo(message: Message, state: FSMContext):
    await state.set_state(AddInfo.new_post)
    await message.answer(text='Загрузите фотографию', reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddInfo.photo)



@admin.message(AdminProtect(), AddInfo.photo)
async def add_description(message: Message, state: FSMContext):
    if not message.photo:
        return await message.answer(text='Загрузить можно только фотографию')
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer(text="Добавьте описание поста")
    await state.set_state(AddInfo.description)



@admin.message(AdminProtect(), AddInfo.description, F.text)
async def add_symbol(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text="Добавьте символ")
    await state.set_state(AddInfo.symbol)



@admin.message(AdminProtect(), AddInfo.symbol, F.text)
async def add_button_1(message: Message, state: FSMContext):
    await state.update_data(symbol=message.text)
    await message.answer(text="Добавьте название первой кнопки")
    await state.set_state(AddInfo.button_1)



@admin.message(AdminProtect(), AddInfo.button_1, F.text)
async def add_button_2(message: Message, state: FSMContext):
    await state.update_data(button_1=message.text)
    await message.answer(text="Добавьте название второй кнопки")
    await state.set_state(AddInfo.button_2)



@admin.message(AdminProtect(), AddInfo.button_2, F.text)
async def add_button_3(message: Message, state: FSMContext):
    await state.update_data(button_2=message.text)
    await message.answer(text="Добавьте название третьей кнопки")
    await state.set_state(AddInfo.button_3)



@admin.message(AdminProtect(), AddInfo.button_3, F.text)
async def set_correct_button(message: Message, state: FSMContext):
    await state.update_data(button_3=message.text)
    
    data = await state.get_data()
    button_1 = data.get('button_1', '1')
    button_2 = data.get('button_2', '2')
    button_3 = data.get('button_3', '3')
    
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button_1, callback_data='correct_button_1')],
        [InlineKeyboardButton(text=button_2, callback_data='correct_button_2')],
        [InlineKeyboardButton(text=button_3, callback_data='correct_button_3')]
    ])
    
    await message.answer(text="Какую кнопку сделать верным ответом?", reply_markup=inline_kb)



@admin.callback_query(AdminProtect(), F.data.startswith('correct_button_'))
async def set_correct_button(callback: CallbackQuery, state: FSMContext):
    correct_button = int(callback.data.split('_')[-1])
    await state.update_data(correct_button=correct_button)
    data = await state.get_data()
    admin_db.add_info(data['photo'], data['description'], data['symbol'], data['button_1'], data['button_2'], data['button_3'], data['correct_button'])
    await send_post_preview(callback.message, data)
    await state.clear()  

#################### create post ####################



#################### edit post ####################

@admin.callback_query(AdminProtect(), F.data == 'edit')
async def edit_options(callback: CallbackQuery):
    edit_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить фотографию", callback_data='edit_photo'), 
         InlineKeyboardButton(text="Изменить первую кнопку", callback_data='edit_button_1')],
        [InlineKeyboardButton(text="Изменить описание", callback_data='edit_description'), 
         InlineKeyboardButton(text="Изменить вторую кнопку", callback_data='edit_button_2')],
        [InlineKeyboardButton(text="Изменить символ", callback_data='edit_symbol'), 
         InlineKeyboardButton(text="Изменить третью кнопку", callback_data='edit_button_3')],
        [InlineKeyboardButton(text="Назад", callback_data='back_to_main')]
    ])
    await callback.message.edit_reply_markup(reply_markup=edit_markup)



@admin.callback_query(AdminProtect(), F.data == 'back_to_main')
async def back_to_main(callback: CallbackQuery):
    main_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить", callback_data='edit')],
        [InlineKeyboardButton(text="Отправить", callback_data='send')],
    ])
    await callback.message.edit_reply_markup(reply_markup=main_markup)



@admin.callback_query(AdminProtect(), F.data.startswith('edit_'))
async def initiate_edit(callback: CallbackQuery, state: FSMContext):
    data_field = callback.data.split('_', 1)[1]
    await state.set_state(getattr(AddInfo, f"edit_{data_field}"))
    await callback.message.answer(f"Отправьте новое значение")



@admin.message(AdminProtect(), AddInfo.edit_photo)
async def process_new_photo(message: Message, state: FSMContext):
    if not message.photo:
        return await message.answer(text='Загрузить можно только фотографию')
    await state.update_data(photo=message.photo[-1].file_id)
    admin_db.update_info('photo', message.photo[-1].file_id)
    await update_message(message, state, "Фотография изменена")
    await state.clear() 



@admin.message(AdminProtect(), AddInfo.edit_description, F.text)
async def process_new_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    admin_db.update_info('description', message.text)
    await update_message(message, state, "Описание изменено")
    await state.clear() 



@admin.message(AdminProtect(), AddInfo.edit_symbol, F.text)
async def process_new_symbol(message: Message, state: FSMContext):
    await state.update_data(symbol=message.text)
    admin_db.update_info('symbol', message.text)
    await update_message(message, state, "Символ изменен")
    await state.clear() 



@admin.message(AdminProtect(), AddInfo.edit_button_1, F.text)
async def process_new_button_1(message: Message, state: FSMContext):
    await state.update_data(button_1=message.text)
    admin_db.update_info('button_1', message.text)
    await update_message(message, state, "Первая кнопка изменена")
    await state.clear() 



@admin.message(AdminProtect(), AddInfo.edit_button_2, F.text)
async def process_new_button_2(message: Message, state: FSMContext):
    await state.update_data(button_2=message.text)
    admin_db.update_info('button_2', message.text)
    await update_message(message, state, "Вторая кнопка изменена")
    await state.clear() 



@admin.message(AdminProtect(), AddInfo.edit_button_3, F.text)
async def process_new_button_3(message: Message, state: FSMContext):
    await state.update_data(button_3=message.text)
    admin_db.update_info('button_3', message.text)
    await update_message(message, state, "Третья кнопка изменена")
    await state.clear() 



async def update_message(message: Message, state: FSMContext, update_text: str):
    data = admin_db.get_info()
    description = data[1]
    symbol = data[2]
    button_1 = data[3]
    button_2 = data[4]
    button_3 = data[5]
    post_text = f"Описание: {description}\nСимвол: {symbol}\nКнопки: {button_1}, {button_2}, {button_3}"
    post_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button_1, callback_data='button_1')],
        [InlineKeyboardButton(text=button_2, callback_data='button_2')],
        [InlineKeyboardButton(text=button_3, callback_data='button_3')]
    ])
    await message.answer_photo(photo=data[0], caption=post_text, reply_markup=post_markup)
    await message.answer(text=update_text)
    await send_edit_options(message)



async def send_edit_options(message: Message):
    edit_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить фотографию", callback_data='edit_photo'), 
         InlineKeyboardButton(text="Изменить первую кнопку", callback_data='edit_button_1')],
        [InlineKeyboardButton(text="Изменить описание", callback_data='edit_description'), 
         InlineKeyboardButton(text="Изменить вторую кнопку", callback_data='edit_button_2')],
        [InlineKeyboardButton(text="Изменить символ", callback_data='edit_symbol'), 
         InlineKeyboardButton(text="Изменить третью кнопку", callback_data='edit_button_3')],
        [InlineKeyboardButton(text="Назад", callback_data='back_to_main')]
    ])
    await message.answer("Выберите действие", reply_markup=edit_markup)

#################### edit post ####################



#################### updated post ####################

async def send_post_preview(message: Message, data):
    main_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить", callback_data='edit')],
        [InlineKeyboardButton(text="Отправить", callback_data='send')],
    ])

    button_1_text = data.get('button_1', 'N/A')
    button_2_text = data.get('button_2', 'N/A')
    button_3_text = data.get('button_3', 'N/A')

    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button_1_text, callback_data='button_1')],
        [InlineKeyboardButton(text=button_2_text, callback_data='button_2')],
        [InlineKeyboardButton(text=button_3_text, callback_data='button_3')]
    ])

    await message.answer_photo(
        data.get('photo'), 
        caption=f"Описание: {data.get('description')}\nСимвол: {data.get('symbol')}\nКнопки: {button_1_text}, {button_2_text}, {button_3_text}", 
        reply_markup=inline_markup
    )
    await message.answer(text="Выберите действие", reply_markup=main_markup)



@admin.callback_query(AdminProtect(), F.data == 'send')
async def send_confirmation(callback: CallbackQuery):
    confirmation_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data='confirm_send_yes'),
            InlineKeyboardButton(text="Нет", callback_data='confirm_send_no')
        ]
    ])
    await callback.message.answer("Вы уверены, что хотите опубликовать пост?", reply_markup=confirmation_markup)



@admin.callback_query(AdminProtect(), F.data == 'confirm_send_no')
async def cancel_post(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()



async def send_post_to_admin(chat_id, data, bot):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=data[3], callback_data='button_1')],
        [InlineKeyboardButton(text=data[4], callback_data='button_2')],
        [InlineKeyboardButton(text=data[5], callback_data='button_3')]
    ])
    await bot.send_photo(chat_id=chat_id, photo=data[0], caption=f"Описание: {data[1]}\nСимвол: {data[2]}", reply_markup=inline_markup)



@admin.callback_query(AdminProtect(), F.data == 'confirm_send_yes')
async def confirm_send(callback: CallbackQuery, bot):
    data = admin_db.get_info()
    await send_post_to_admin(callback.message.chat.id, data, bot)
    save_post_data(data)
    await callback.message.answer("Пост опубликован!")



async def send_saved_post(message: Message, bot):
    data = get_saved_post_data()
    if data:
        inline_markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=data[3], callback_data='button_1')],
            [InlineKeyboardButton(text=data[4], callback_data='button_2')],
            [InlineKeyboardButton(text=data[5], callback_data='button_3')]
        ])
        await bot.send_photo(chat_id=message.chat.id, photo=data[0], caption=data[1], reply_markup=inline_markup)

#################### updated post ####################



#################### Vote ####################

last_vote_times = {}

@admin.callback_query(F.data.startswith('button_'))
async def handle_vote(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    if user_id in last_vote_times:
        last_vote_time = last_vote_times[user_id]
        if (datetime.now() - last_vote_time) < timedelta(minutes=1):
            await callback.answer("Голосовать можно раз в минуту.", show_alert=True)
            return

    data = admin_db.get_info()
    user = callback.from_user
    selected_button = int(callback.data.split('_')[-1])

    if selected_button == data[6]:  # data[6] - кнопка верного ответа
        if data[2] in user.username:  # data[2] - символ в нике
            user_db.add_user(user.id, user.username, selected_button)
            await callback.answer("Вы правильно ответили!")
        else:
            await callback.answer("Вы правильно ответили, но ваш никнейм не содержит требуемый символ.")
    else:
        await callback.answer("Вы ответили неверно.")
    
    last_vote_times[user_id] = datetime.now()

#################### Vote ####################
