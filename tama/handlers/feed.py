from aiogram import types
from users import save_pet
from .utils import get_pet, get_pet_or_reply
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tamagogo import Tamago
from game_data.items import ITEMS

buttons_per_row = 4

def food_keyboard(pet):
    buttons = []

    for item_id, item in ITEMS.items():
        if item["type"] != "food":
            continue

        # Базовые продукты (бесконечные)
        if item.get("is_base"):
            buttons.append(
                InlineKeyboardButton(
                    text=f"{item['name']} ∞",
                    callback_data=f"feed_{item_id}"
                )
            )

        # Из инвентаря
        elif item_id in pet.inventory:
            buttons.append(
                InlineKeyboardButton(
                    text=f"{item['name']} ({pet.inventory[item_id]})",
                    callback_data=f"feed_{item_id}"
                )
            )

    # Группировка по 4 кнопки
    rows = [buttons[i:i+4] for i in range(0, len(buttons), 4)]
    return InlineKeyboardMarkup(inline_keyboard=rows)

async def feed_callback_handler(callback: types.CallbackQuery):
    pet = await get_pet_or_reply(callback)
    if not pet:
        return

    item_id = callback.data.replace("feed_", "")
    item = ITEMS.get(item_id)

    if not item:
        await callback.answer("❌ Предмет не найден", show_alert=True)
        return

    # 🔹 БАЗОВАЯ ЕДА
    if item.get("is_base"):  # Если это бесконечная еда
        pet.feed(item["amount"])
        save_pet(callback.from_user.id, pet)

        await callback.message.edit_text(
            f"{item['name']} съедено!\n"
            f"+{item['amount']} к сытости"
        )
        await callback.answer()
        return

    # 🔹 ИЗ ИНВЕНТАРЯ (обычные предметы)
    result = pet.use_item(item_id)
    if result != "ok":
        await callback.answer("❌ У тебя нет этого предмета", show_alert=True)
        return

    save_pet(callback.from_user.id, pet)
    await callback.message.edit_text(
        f"{item['name']} использовано!\n"
        f"+{item['amount']} к сытости"
    )
    await callback.answer()

async def show_food_options(message: types.Message):
    pet = await get_pet_or_reply(message)
    if not pet:
        return

    kb = food_keyboard(pet)
    await message.answer("🍽 Чем покормить питомца?", reply_markup=kb)