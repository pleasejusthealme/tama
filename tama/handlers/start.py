from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from users import get_pet, create_pet, delete_pet

def look_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🐶', callback_data='look_dog'),
                InlineKeyboardButton(text='🐷', callback_data='look_pig'),
                InlineKeyboardButton(text='🦐', callback_data='look_shrimp'),
                InlineKeyboardButton(text='🐱', callback_data='look_cat'),
            ],
            [
                InlineKeyboardButton(text='🐥', callback_data='look_bird'),
                InlineKeyboardButton(text='👽', callback_data='look_alien'),
                InlineKeyboardButton(text='🐸', callback_data='look_frog'),
            ]
        ]
    )

async def start_handler(message: types.Message):
    user_id = message.from_user.id
    pet = get_pet(user_id)

    if pet:
        if pet.is_alive:
            await message.answer('🐾 Кажется, у тебя уже есть питомец!')
            return
        else:
            delete_pet(user_id)
    
    await message.answer(
        "🥚 Выбери, кем будет твой питомец:",
        reply_markup=look_keyboard()
    )

async def look_choice_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    look_map = {
        "look_dog": "🐶",
        "look_pig": "🐷",
        "look_shrimp": "🦐",
        "look_cat": "🐱",
        "look_bird": "🐥",
        "look_alien": "👽",
        "look_frog": "🐸"
    }

    look = look_map.get(callback.data)
    if not look:
        return
    
    create_pet(user_id, look)

    await callback.message.edit_text(
        f"🎉 У тебя появился питомец {look}!\n"
        "Дай ему имя командой /name (например: /name Тама)"
    )

    await callback.answer()

def register_start_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command(commands=["start"]))
    dp.callback_query.register(
    look_choice_handler,
    F.data.startswith("look_")
    )