from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import  FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard= True)
button = KeyboardButton(text = "Рассчитать")
button2 = KeyboardButton(text="Информация")

kb.add(button, button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup=kb)



@dp.message_handler(text = "Рассчитать")
async def set_age(message):
    await message.answer("Введите свой возраст")
    await UserState.age.set()

@dp.message_handler()
async def all_massages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = int(message.text))
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = int(message.text))
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = int(message.text))

    data = await state.get_data()
    formula = 10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] - 161
    await message.answer(f"Ваша норма калорий {formula}")
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)