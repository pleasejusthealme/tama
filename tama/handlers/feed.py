from aiogram import types
from users import save_pet
from .utils import get_pet, get_pet_or_reply
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tamagogo import Tamago
from game_data.items import ITEMS

buttons_per_row = 4

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

    await callback.message.edit_text(f"🍖 Спасибо, что покормил меня! \n+{gained} к сытости!")
    await callback.answer()

async def show_food_options(message: types.Message):
    pet = await get_pet_or_reply(message)
    if not pet:
        return

    kb = InlineKeyboardMarkup(row_width = buttons_per_row)

    base_items = [item_id for item_id, item in ITEMS.items() if item.get("is_base", False)]
    base_buttons = [
        InlineKeyboardButton(
            text=f"{ITEMS[item_id['name']]} {ITEMS[item_id].get('amount', '')}",
            callback_data = f"feed_{item_id}"
        ) for item_id in base_items
    ]

    inventory_buttons = []
    for item_id, count in pet.inventory.items():
        item = ITEMS.get(item_id)
        if item:
            inventory_buttons.append(
                InlineKeyboardButton(
                    text = f"{item['name']} ({count})",
                    callback_data = f"feed_{item_id}"
                )
            )

    all_buttons = base_buttons + inventory_buttons
    kb.add(*all_buttons)

    await message.answer("Выбери, чем меня покормить:", reply_markup=kb)
