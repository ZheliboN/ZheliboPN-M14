from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ''
formula = '10 x вес(кг) + 6,25 x рост(см) - 5 x возраст(лет) + 5'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()
kb.resize_keyboard = True
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.row(button1, button2)
kb.add(button3)
del_kb = ReplyKeyboardRemove()

inline_kb = InlineKeyboardMarkup()
inline_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(inline_button1, inline_button2)

price_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продукт1', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт2', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт3', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт4', callback_data='product_buying')]
    ]
)


def do_miflin_san_zheor(age, growth, weight):
    calorie = 10*int(weight)+6.25*int(growth)-5*int(age)+5
    return calorie


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(formula)
    await call.answer()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for number in range(1, 5):
        await message.answer(f'Название: Продукт {number} | Описание: описание {number} | Цена: {number*100}')
        with open(f'img/vitamin{number}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=price_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:', reply_markup=kb)
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calorie = do_miflin_san_zheor(data['age'], data['growth'], data['weight'])
    await message.answer(f'Норма каллорий: {calorie}')
    await message.answer('Спасибо за работу!', reply_markup=del_kb)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
