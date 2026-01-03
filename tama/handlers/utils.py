from aiogram import types
from users import get_pet, save_pet
from tamagogo import Tamago

async def get_alive_pet(message: types.Message) -> Tamago | None:
    user_id = message.from_user.id
    pet = get_pet(user_id)

    if pet is None:
        await message.answer("Кажется, у тебя нет питомца... Сначала напиши /start")
        return None
    
    pet.lazy_update()
    
    if not pet.is_alive:
        save_pet(user_id, pet)
        await message.answer(f"💀 {pet.name} умер... Напиши /start, чтобы завести нового питомца.")
        return None
        
    save_pet(user_id, pet)
    return pet