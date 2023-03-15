import logging

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

logging.basicConfig(level=logging.INFO)

bot = Bot('2069529975:AAGy10JUdPwSMVVDfcAfM66ZldNw11l20uo')
dp = Dispatcher(bot)

db = SQLighter('db.db')

@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)
    await message.answer('Вы успешно подписались на рассылку!')

@dp.message_handler(commands=['unsubscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id, False)
        await message.answer('Вы и так не подписаны!')
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer('Вы успешно отписались от рассылки!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)