from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

inline_kb = types.ReplyKeyboardMarkup(
    keyboard=[
            [
                types.KeyboardButton(text='💡 Картинка'),
                types.KeyboardButton(text='🏞 Погода'),
            ],
            [
                types.KeyboardButton(text='💡 Курс валют'),
                types.KeyboardButton(text='🏞 Список фильмов'),
            ],
            [
                types.KeyboardButton(text='💡 Шутка'),
                types.KeyboardButton(text='🏞 Пройти опрос'),
            ],
        ],
        resize_keyboard=True,
)
image_kb = types.ReplyKeyboardMarkup(
    keyboard=[
            [
                types.KeyboardButton(text="Футбол⚽"),
            ],
            [
                types.KeyboardButton(text="Бокс🥊"),
            ],
            [
                types.KeyboardButton(text="Баскетбол🏀"),
            ],
        ],
            resize_keyboard=True,
)
exchangerate_kb = types.ReplyKeyboardMarkup(
    keyboard=[
            [
                types.KeyboardButton(text="USD🇺🇸"),
            ],
            [
                types.KeyboardButton(text="EUR🇪🇺"),
            ],
            [
                types.KeyboardButton(text="RUB🇷🇺"),
            ],
            [
                types.KeyboardButton(text="KZT🇰🇿"),
            ],
            [
                types.KeyboardButton(text="CNY🇨🇳"),
            ],
            [
                types.KeyboardButton(text="GBP🇬🇧"),
            ]
        ],
            resize_keyboard=True,
)