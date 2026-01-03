from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from .utils import get_alive_pet
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
    pet = await get_alive_pet(message)
    if not pet:
        return
    
    await message.answer(
        f"😴 {pet.name} сейчас спит! Ничего нельзя делать, пока он не проснется.",
        reply_markup=wake_up()
    )

async def wake_callback(callback: types.CallbackQuery):
    pet = await get_alive_pet(callback.message)

    if not pet:
        return
    
    if not pet.is_sleeping:
        await callback.answer("А кого будить собрались?", show_alert=True)
        return

    pet.wake_up()  # метод, который устанавливает is_sleeping = False и восстанавливает энергию
    save_pet(callback.from_user.id, pet)

    await callback.message.edit_text(f"🌞 {pet.name} проснулся и снова полон энергии!")
    await callback.answer()