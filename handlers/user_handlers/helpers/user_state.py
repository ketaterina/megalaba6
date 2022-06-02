from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStateMainMenu(StatesGroup):
    start_menu = State()
    start_menu_work_data = State()
    start_menu_work_db = State()
    start_menu_admin = State()
    start_menu_work_db_add_album = State()
    start_menu_work_db_add_song = State()
    start_menu_workd_db_add_song_to_album = State()