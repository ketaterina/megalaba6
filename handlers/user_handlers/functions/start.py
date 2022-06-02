from aiogram.utils.helper import Helper
from database.functions import DataBaseFunc
from database.models import User, Message
from mics import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import DELEMITER, get_text
from handlers.user_handlers.helpers.generator_keyboards import UserGeneratorKeyboard
from handlers.admin_handlers.helpers.generator_keyboards import AdminGeneratorKeyboard
from handlers.user_handlers.helpers.user_state import UserStateMainMenu
from handlers.user_handlers.helpers.help import get_call_data
import re


@dp.message_handler(commands=['start'], state='*')
async def start_message(message: types.Message):
    """Обработчик команды /start."""
    user = DataBaseFunc.get_user(message.from_user.id, message.from_user)
    await DataBaseFunc.delete_messages(user)

    if not user.chat_id:
        user.chat_id = message.chat.id

    await message.delete()
    mess = await message.answer(get_text('start_menu'), reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user, 'start_menu'))
    await DataBaseFunc.delete_messages(user)

    ms = Message(user_id=user.id, message_id=mess.message_id)
    DataBaseFunc.add(ms)
    await UserStateMainMenu.main_menu.set()


# region Callback на кнопки
@dp.callback_query_handler(lambda callback: callback.data == "start_menu_&work_db_&add_song", state='*')
async def add_song_to_db(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    call_data = get_call_data(callback.data)

    await callback.message.edit_text(get_text(call_data), reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user, call_data))
    state = getattr(UserStateMainMenu, call_data.replace(DELEMITER, ''))
    await state.set()


@dp.callback_query_handler(lambda callback: callback.data == "start_menu_&work_db_&add_album", state='*')
async def add_song_to_db(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    call_data = get_call_data(callback.data)

    await callback.message.edit_text(get_text(call_data), reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user, call_data))
    state = getattr(UserStateMainMenu, call_data.replace(DELEMITER, ''))
    await state.set()


@dp.callback_query_handler(lambda callback: callback.data == "start_menu_&work_db_&add_song_to_album", state='*')
async def add_song_to_album(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    call_data = get_call_data(callback.data)

    await callback.message.edit_text(get_text(call_data), reply_markup=await UserGeneratorKeyboard.get_keyboard_add_song_to_album(user, call_data))


@dp.callback_query_handler(lambda callback: "album@" in callback.data, state='*')
async def add_song_in_album_final(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    song_id = int(re.search(pattern="song@\d+",
                  string=callback.data).group().replace('song@', ''))
    album_id = int(re.search(pattern="album@\d+",
                   string=callback.data).group().replace('album@', ''))

    song = DataBaseFunc.get_song(song_id)
    album = DataBaseFunc.get_album(album_id)

    album.songs.append(song)
    DataBaseFunc.commit()

    await callback.message.edit_text(f"Песня \"{song.name}\" добавлена в альбом \"{album.name}\"",
                                     reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user, "start_menu_&work_db"))


@dp.callback_query_handler(lambda callback: "song@" in callback.data, state='*')
async def add_song_in_album(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    call_data = get_call_data(callback.data)

    await callback.message.edit_text(get_text("start_menu_&work_db_&add_song_to_album_get_album"),
                                     reply_markup=await UserGeneratorKeyboard.get_keyboard_add_albums(user, call_data))


@dp.callback_query_handler(lambda callback: callback.data == "song_in_album_back", state='*')
async def add_song_in_album_final(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)

    await callback.message.edit_text(get_text("start_menu_&work_db"),
                                     reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user, "start_menu_&work_db"))
    

@dp.callback_query_handler(lambda callback: callback.data == "start_menu_&admin_&add_user")
async def add_user(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text("admin_menu_add_user"), reply_markup= await AdminGeneratorKeyboard.get_add_admin( "admin_menu_add_user"))
    

@dp.callback_query_handler(lambda callback: "start_menu" in callback.data, state="*")
async def start_menu_handler(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    call_data = get_call_data(callback.data)
    await callback.message.edit_text(get_text(call_data), reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user, call_data))

# endregion


# region MessageHandlers
@dp.message_handler(state=UserStateMainMenu.start_menu_work_db_add_song, content_types=types.ContentTypes.TEXT)
async def add_name_song(message: types.Message):
    """Ввод имени новой песни"""
    user = DataBaseFunc.get_user(message.from_user.id)
    try:
        DataBaseFunc.add_song(message.text)
        data = "start_menu_&work_db"
        await bot.send_message(chat_id=user.chat_id, text=get_text(data), reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user, data))
        state = getattr(UserStateMainMenu, data.replace(DELEMITER, ''))
        await state.set()
    except Exception as exc:
        await bot.send_message(chat_id=user.chat_id, text=f"{str(exc)}. Попробуйте еще раз.")


@dp.message_handler(state=UserStateMainMenu.start_menu_work_db_add_album, content_types=types.ContentTypes.TEXT)
async def add_name_album(message: types.Message):
    """Ввод имени нового альбома"""
    user = DataBaseFunc.get_user(message.from_user.id)
    try:
        DataBaseFunc.add_album(message.text)
        data = "start_menu_&work_db"
        await bot.send_message(chat_id=user.chat_id, text=get_text(data), reply_markup=await UserGeneratorKeyboard.get_keyboard_inline(user, data))
        state = getattr(UserStateMainMenu, data.replace(DELEMITER, ''))
        await state.set()
    except Exception as exc:
        await bot.send_message(chat_id=user.chat_id, text=f"{str(exc)}. Попробуйте еще раз.")

@dp.message_handler(state='*')
async def delete_mess(message: types.Message):
    await message.delete()
# endregion
