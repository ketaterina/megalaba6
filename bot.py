import handlers
from mics import dp
from aiogram import executor

from database.functions import DataBaseFunc

if __name__ == '__main__':
    DataBaseFunc.drop_all()
    DataBaseFunc.add_main_admin()

    executor.start_polling(dp)
