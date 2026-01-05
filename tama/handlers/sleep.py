from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from .utils import get_pet_or_reply
from users import save_pet
from tamagogo import Tamago

def wake_up():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⏰ Разбудить",
                    callback_data="wake_up"
                )
            ]
        ]
    )

async def pet_is_sleeping(message: types.Message):
    pet = await get_pet_or_reply(message)
    if not pet:
        return

    await message.answer(
        f"😴 {pet.name} сейчас спит! Ничего нельзя делать, пока он не проснется.",
        reply_markup=wake_up()
    )

async def wake_callback(callback: types.CallbackQuery):
    pet = await get_pet_or_reply(callback, allow_sleeping=True)
    if not pet:
        return

    pet.wake_up()
    save_pet(callback.from_user.id, pet)

    await callback.message.edit_text(f"🌞 {pet.name} проснулся и снова полон энергии!")
    await callback.answer()
