from aiogram.utils.helper import Helper
from database.functions import DataBaseFunc
from database.models import User, Message
from mics import dp, bot
from aiogram import types
from config import DELEMITER, get_text
from handlers.user_handlers.helpers.generator_keyboards import UserGeneratorKeyboard
from handlers.admin_handlers.helpers.generator_keyboards import AdminGeneratorKeyboard
from handlers.user_handlers.helpers.help import get_call_data
import re


@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_back_add_user")
async def add_user_back(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text("start_menu_&admin"), reply_markup= await UserGeneratorKeyboard.get_keyboard_inline(user, "start_menu_&admin"))


@dp.callback_query_handler(lambda callback:  "start_menu_&admin_&add_user_@" in callback.data)
async def add_user_id(callback: types.CallbackQuery):
    await callback.answer()
    user_id = int(re.search(pattern="user_@\d+", string=callback.data).group().replace('user_@', ""))
    user = DataBaseFunc.get_user(user_id)
    user.is_admin = True
    DataBaseFunc.commit()
    await callback.message.edit_text(f"Пользователь {user.username} назначен администратором",
                                     reply_markup=await AdminGeneratorKeyboard.get_add_admin( "start_menu_&admin"))


@dp.callback_query_handler(lambda callback: "admin_menu" in callback.data, state="*")
async def admin_menu_handler(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    call_data = get_call_data(callback.data)
    await callback.message.edit_text(get_text(call_data), reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user, call_data))