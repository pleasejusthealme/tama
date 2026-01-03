from aiogram import types
from users import save_pet
from .utils import get_pet, get_alive_pet
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def food_keyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🍎", callback_data="feed_apple"),
                InlineKeyboardButton(text="🥩", callback_data="feed_meat")
            ],
            [
                InlineKeyboardButton(text="🥕", callback_data="feed_carrot"),
                InlineKeyboardButton(text="🍪", callback_data="feed_cookie")
            ]
        ]
    )
    return kb

async def feed_callback_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    pet = get_pet(user_id)
    if not pet or not pet.is_alive:
        await callback.answer("Кажется, у тебя нет питомца или он умер :(", show_alert=True)
        return
    
    food_values = {
        "feed_apple": 1,
        "feed_carrot": 1,
        "feed_cookie": 2,
        "feed_meat": 3
    }

    amount = food_values.get(callback.data, 1)
    before = pet.hunger
    pet.feed(amount)
    save_pet(callback.from_user.id, pet)
    gained = pet.hunger - before
    
    await callback.message.edit_text(f"🍖 Спасибо, что покормил меня! \n+{gained} к сытости")
    await callback.answer()

async def show_food_options(message: types.Message):
    pet = await get_alive_pet(message)
    if not pet:
        return
    await message.answer("Выбери что я съем:", reply_markup=food_keyboard())
