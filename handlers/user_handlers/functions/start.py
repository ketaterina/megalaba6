
from aiogram.utils.helper import Helper
from database.functions import DataBaseFunc
from database.models import User, Message
from mics import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import DELEMITER, get_text
from handlers.user_handlers.helpers.generator_keyboards import UserGeneratorKeyboard
from handlers.user_handlers.helpers.user_state import UserStateMainMenu
from handlers.user_handlers.helpers.help import get_call_data


@dp.message_handler(commands=['start'], state='*')
async def start_message(message: types.Message):
    """Обработчик команды /start."""
    user = DataBaseFunc.get_user(message.from_user.id, message.from_user)

    if not user.chat_id:
        user.chat_id = message.chat.id

    await message.delete()
    mess = await message.answer(get_text('start_menu'), reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user,'start_menu'))
    await DataBaseFunc.delete_messages(user)

    ms = Message(user_id=user.id, message_id=mess.message_id)
    DataBaseFunc.add(ms)
    await UserStateMainMenu.main_menu.set()


@dp.callback_query_handler(lambda callback: "start_menu" in callback.data, state = "*")
async def start_menu_handler(callback : types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    call_data = get_call_data(callback.data)
    await callback.message.edit_text(get_text(call_data), reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user, call_data))
    
    try:
        state = getattr(UserStateMainMenu, call_data.replace(DELEMITER, ''))
        await state.set()
    except:
        pass
