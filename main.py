import asyncio
import os

from aiogram.client.session import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup

from db import Database
from keyboards import inline_kb, image_kb, exchangerate_kb


load_dotenv()

TOKEN = os.getenv('TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

bot = Bot(token=TOKEN)
dp = Dispatcher()
db = Database(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)


@dp.message(CommandStart())
async def start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f'Привет, {user_name}!', reply_markup=inline_kb)



@dp.message(F.text == "💡 Картинка")
async def send_image_menu(message: Message):
    await message.answer('Выберите фото:', reply_markup=image_kb)

@dp.message(F.text == 'Назад')
async def backkb(message: Message):
    await message.answer('Возвращаю назад', reply_markup=inline_kb)


@dp.message(F.text == "Футбол⚽")
async def send_football_image(message: Message):
    f = FSInputFile("ftbl.jpg")
    await message.answer_photo(f)


@dp.message(F.text == "Бокс🥊")
async def send_boxing_image(message: Message):
    b = FSInputFile("box.jpg")
    await message.answer_photo(b)


@dp.message(F.text == "Баскетбол🏀")
async def send_basketball_image(message: Message):
    b1 = FSInputFile("bskt.jpg")
    await message.answer_photo(b1)


@dp.message(F.text == "🏞 Погода")
async def get_weather(message: Message):
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Bishkek&appid={WEATHER_API_KEY}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                type_ = data["weather"][0]["main"]
                temp_c = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                city = data["name"]
                # Отправляем информацию о погоде пользователю
                await message.answer(f"Погода в городе {city}:\n{type_}\nТемпература: {temp_c}°C\nЧувствуется как: {feels_like}°C")
            else:
                await message.answer("Произошла ошибка при получении данных о погоде.")



@dp.message(F.text == '💡 Курс валют')
async def get_exchangerate(message: Message):
    await message.answer('Выберите валюту: ', reply_markup=exchangerate_kb)


@dp.message(F.text == 'USD🇺🇸')
async def usd(message: Message):
    await message.answer(f'Покупка 86.70 \nПродажа	87.10')

@dp.message(F.text == 'EUR🇪🇺')
async def eur(message: Message):
    await message.answer(f'Покупка 93.50 \nПродажа	94.00')

@dp.message(F.text == 'RUB🇷🇺')
async def rub(message: Message):
    await message.answer(f'Покупка 1.005 \nПродажа	1.020')

@dp.message(F.text == 'KZT🇰🇿')
async def kzt(message: Message):
    await message.answer(f'Покупка 0.1229 \nПродажа 0.1750')

@dp.message(F.text == 'CNY🇨🇳')
async def cny(message: Message):
    await message.answer(f'Покупка 11.80 \nПродажа 12.40')

@dp.message(F.text == 'GBP🇬🇧')
async def gbp(message: Message):
    await message.answer(f'Покупка 109.00 \nПродажа 111.00')
@dp.message(F.text == 'Назад')
async def backkb(message: Message):
    await message.answer('Возвращаю назад', reply_markup=inline_kb)


@dp.message(F.text == '🏞 Список фильмов')
async def send_movies(message: Message):
    await message.answer('Список фильмов:\n1 - Интерстеллар (Interstellar, 2014) – Фантастика, драма \n2 - Начало (Inception, 2010) – Фантастика, триллер\n3 - Зеленая миля (The Green Mile, 1999) – Драма, фэнтези\n4 - Побег из Шоушенка (The Shawshank Redemption, 1994) – Драма\n5 - Джентльмены (The Gentlemen, 2019) – Криминальная комедия')

class Survey(StatesGroup):
    name = State()
    age = State()
    subject = State()
    color = State()
    movie = State()
    hobby = State()
    dream = State()
    country = State()

@dp.message(F.text == '💡 Шутка')
async def send_joke(message: Message):
    url = "https://v2.jokeapi.dev/joke/Any"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                joke_data = await response.json()

                if joke_data["type"] == "single":
                    joke = joke_data["joke"]
                else:
                    joke = f'{joke_data["setup"]}\n\n{joke_data["delivery"]}'

                await message.answer(joke)
            else:
                await message.answer("Ошибка при получении шутки. Попробуйте позже.")


@dp.message(F.text == 'Назад')
async def backkb(message: Message):
    await message.answer('Возвращаю назад', reply_markup=inline_kb)


@dp.message(F.text == "🏞 Пройти опрос")
async def start_survey(message: Message, state: FSMContext):
    await state.set_state(Survey.name)
    await message.answer("Как вас зовут?")


@dp.message(Survey.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Survey.age)
    await message.answer("Сколько вам лет?")


@dp.message(Survey.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Survey.subject)
    await message.answer("Какой ваш любимый школьный предмет?")


@dp.message(Survey.subject)
async def process_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(Survey.color)
    await message.answer("Какой ваш любимый цвет?")


@dp.message(Survey.color)
async def process_color(message: Message, state: FSMContext):
    await state.update_data(color=message.text)
    await state.set_state(Survey.movie)
    await message.answer("Какой ваш любимый фильм?")


@dp.message(Survey.movie)
async def process_movie(message: Message, state: FSMContext):
    await state.update_data(movie=message.text)
    await state.set_state(Survey.hobby)
    await message.answer("Какое у вас хобби?")


@dp.message(Survey.hobby)
async def process_hobby(message: Message, state: FSMContext):
    await state.update_data(hobby=message.text)
    await state.set_state(Survey.dream)
    await message.answer("О чем вы мечтаете?")


@dp.message(Survey.dream)
async def process_dream(message: Message, state: FSMContext):
    await state.update_data(dream=message.text)
    await state.set_state(Survey.country)
    await message.answer("В какой стране вы мечтаете побывать?")


@dp.message(Survey.country)
async def process_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    data = await state.get_data()

    # Сохраняем данные в PostgreSQL
#    conn = await db.connect()
#    await conn.execute(
#        'INSERT INTO survey_results (name, age, subject, color, movie, hobby, dream, country) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
#        data['name'], data['age'], data['subject'], data['color'], data['movie'], data['hobby'], data['dream'],
#        data['country']
#    )
#    await conn.close()

    # Выводим результаты пользователю
    result = (f"Результаты опроса:\n"
              f"Имя: {data['name']}\n"
              f"Возраст: {data['age']}\n"
              f"Любимый предмет: {data['subject']}\n"
              f"Любимый цвет: {data['color']}\n"
              f"Любимый фильм: {data['movie']}\n"
              f"Хобби: {data['hobby']}\n"
              f"Мечта: {data['dream']}\n"
              f"Страна мечты: {data['country']}")

    await message.answer(result)
    await state.clear()





async def main():
    print('Bot started...')
    await db.connect()
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(e)
    finally:
        await db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())