from aiogram import types
from users import get_pet, save_pet
from tamagogo import Tamago

async def get_pet_or_reply(
    event: types.Message | types.CallbackQuery,
    allow_sleeping: bool = False
    ) -> Tamago | None:

    user = event.from_user
    pet = get_pet(user.id)

    if pet is None:
        text = "Кажется, у тебя нет питомца... Сначала напиши /start"
    elif not pet.is_alive:
        text = f"{pet.name} умер..."
    elif pet.is_sleeping and not allow_sleeping:
        text = f"{pet.name} сейчас спит!"
    else:
        pet.lazy_update()
        save_pet(user.id, pet)
        return pet

    if isinstance(event, types.CallbackQuery):
        await event.answer(text, show_alert = True)
    else:
        await event.answer(text)

    return None
