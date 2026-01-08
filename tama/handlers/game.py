from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from users import save_pet, get_pet
from tamagogo import Tamago
from .feed import show_food_options, feed_callback_handler
from .utils import get_pet_or_reply
from .sleep import wake_callback, pet_is_sleeping, wake_up
from game_data.items import ITEMS
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def tama_handler(message: types.Message):
    pet = await get_pet_or_reply(message)
    if not pet:
        return

    hunger_emoji_count = pet.hunger // 2
    happiness_emoji_count = pet.happiness // 2
    energy_emoji_count = pet.energy // 2
    dirty_emoji_count = pet.dirty // 2

    await message.answer(
        f"{pet.look} Привет, я твой {pet.name}!\n\n"
        f"🍖 Сытость: ({pet.hunger}/10)\n"
        f"🌟 Настроение: ({pet.happiness}/10)\n"
        f"⚡ Энергия: ({pet.energy}/10)\n"
        f"💩 Грязь: ({pet.dirty}/10)"
    )

async def inventory_handler(message: types.Message):
    pet = await get_pet_or_reply(message)
    if not pet:
        return

    text = f"Инвентарь {pet.name}:\n{pet.get_inventory_text()}"
    await message.answer(text)

def shop_keyboard() -> InlineKeyboardMarkup:
    kb = []
    row = []

    for item_id, item in ITEMS.items():
        row.append(
        InlineKeyboardButton(
            text = f"{item['name']} ({item['price']})",
            callback_data=f"buy_{item_id}"
            )
        )

        if len(row) == 2:
            kb.append(row)
            row = []

    if row:
        kb.append(row)

    return InlineKeyboardMarkup(inline_keyboard=kb)

async def shop_handler(message: types.Message):
    await message.answer("Магазин:", reply_markup=shop_keyboard())

async def buy_callback(callback):
    pet = await get_pet_or_reply(callback, allow_sleeping=True)
    if not pet:
        return

    item_id = callback.data.replace("buy_", "")
    item = ITEMS.get(item_id)

    if not item:
        await callback_answer("Товар не найден", show_alert=True)
        return

    price = item["price"]

    if pet.coins < price:
        await callback.answer("Недостаточно денег", show_alert=True)
        return

    pet.coins -= price
    pet.add_item(item_id)
    save_pet(callback.from_user.id, pet)

    await callback.answer(f"Куплено {item['name']}")

async def feed_handler(message: types.Message):
    await show_food_options(message)

async def play_handler(message: types.Message):
    pet = await get_pet_or_reply(message)
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
    pet = await get_pet_or_reply(message)
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
    pet = await get_pet_or_reply(message)
    if not pet:
        return

    pet.clean()
    save_pet(message.from_user.id, pet)
    await message.answer(f"🛁 {pet.name} теперь чистый!")

async def sleep_handler(message: types.Message):
    pet = await get_pet_or_reply(message)
    if not pet:
        return

    pet.sleep()
    save_pet(message.from_user.id, pet)
    await message.answer(
        f"😴 {pet.name} сейчас спит! Ничего нельзя делать, пока он не проснется.",
        reply_markup=wake_up()
    )

def register_game_handlers(dp: Dispatcher):
    dp.message.register(tama_handler, Command(commands=["tama"]))
    dp.message.register(sleep_handler, Command(commands=["sleep"]))
    dp.message.register(clean_handler, Command(commands=["clean"]))
    dp.message.register(feed_handler, Command(commands=["feed"]))
    dp.message.register(play_handler, Command(commands=["play"]))
    dp.message.register(name_handler, Command(commands=["name"]))
    dp.message.register(inventory_handler, Command(commands=["inventory"]))
    dp.message.register(shop_handler, Command(commands=["shop"]))
    dp.callback_query.register(feed_callback_handler,F.data.startswith("feed_"))
    dp.callback_query.register(wake_callback, F.data == "wake_up")
    dp.callback_query.register(buy_callback, F.data.startswith("buy_"))
