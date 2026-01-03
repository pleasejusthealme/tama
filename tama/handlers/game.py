from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from users import save_pet, get_pet
from tamagogo import Tamago
from .feed import show_food_options, feed_callback_handler
from .utils import get_alive_pet
from .sleep import wake_callback, pet_is_sleeping, wake_up


# ------------------- ХЕНДЛЕРЫ -------------------

async def status_handler(message: types.Message):
    pet = await get_alive_pet(message)
    if not pet:
        return
    
    hunger_emoji_count = pet.hunger // 2
    happiness_emoji_count = pet.happiness // 2
    energy_emoji_count = pet.energy // 2
    dirty_emoji_count = pet.dirty // 2

    await message.answer(
        f"{pet.look} {pet.name}\n"
        f"Сытость: {'🍖' * hunger_emoji_count} ({pet.hunger}/10)\n"
        f"Настроение: {'🌟' * happiness_emoji_count} ({pet.happiness}/10)\n"
        f"Усталость: {'😴' * energy_emoji_count} ({pet.energy}/10)\n"
        f"Грязь: {'💩' * dirty_emoji_count} ({pet.dirty}/10)"
    )

async def feed_handler(message: types.Message):
    await show_food_options(message)

async def play_handler(message: types.Message):
    pet = await get_alive_pet(message)
    if not pet:
        return
    
    if pet.is_sleeping:
        await pet_is_sleeping(message, pet)
        return
    
    if pet.energy <= 0:
        await message.answer("😴 Я слишком устал, чтобы играть. Отправь меня спать!")

    before = pet.happiness
    pet.play()
    pet.energy -=2
    if pet.energy < 0:
        pet.energy = 0

    save_pet(message.from_user.id, pet)

    gained = pet.happiness - before
    await message.answer(f"🌟 Спасибо, что поиграл со мной! \n +{gained} к настроению!")

async def name_handler(message: types.Message, command: Command):
    pet = await get_alive_pet(message)
    if not pet:
        return

    if not command.args:
        await message.answer("Напиши имя после команды, например: /name Тама")
        return

    new_name = command.args.strip()[:20]
    pet.name = new_name
    save_pet(message.from_user.id, pet)
    await message.answer(f"✅ Имя питомца изменено на {pet.name}!")

async def clean_handler(message: types.Message):
    pet = await get_alive_pet(message)
    if not pet:
        return

    pet.clean()
    save_pet(message.from_user.id, pet)
    await message.answer(f"🛁 {pet.name} теперь чистый!")

async def sleep_handler(message: types.Message):
    pet = await get_alive_pet(message)
    if not pet:
        return
    
    if pet.is_sleeping:
        await message.answer(f"😴 {pet.name} уже спит!")
        return

    pet.sleep()  # метод из tamagogo.py
    save_pet(message.from_user.id, pet)
    await message.answer(
        f"😴 {pet.name} сейчас спит! Ничего нельзя делать, пока он не проснется.",
        reply_markup=wake_up()  # кнопка "Разбудить"
    )

def register_game_handlers(dp: Dispatcher):
    
    dp.message.register(status_handler, Command(commands=["tama"]))
    dp.message.register(sleep_handler, Command(commands=["sleep"]))
    dp.message.register(clean_handler, Command(commands=["clean"]))
    dp.message.register(feed_handler, Command(commands=["feed"]))
    dp.message.register(play_handler, Command(commands=["play"]))
    dp.message.register(name_handler, Command(commands=["name"]))
    dp.callback_query.register(
    feed_callback_handler,
    F.data.startswith("feed_")
    )
    dp.callback_query.register(wake_callback, F.data == "wake_up")
