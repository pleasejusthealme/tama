from tinydb import TinyDB, Query
from config import DB_PATH
from tamagogo import Tamago

db = TinyDB(DB_PATH, indent = 4, sort_keys = True)
User = Query()

def get_pet(user_id: int):
    result = db.get(User.user_id == user_id)
    if result:
        return Tamago.from_dict(result["pet"])
    return None

def save_pet(user_id: int, pet: Tamago):
    data = {"user_id": user_id, "pet": pet.to_dict()}
    if db.get(User.user_id == user_id):
        db.update(data, User.user_id == user_id)
    else:
        db.insert(data)

def create_pet(user_id: int, look: str):
    pet = Tamago(name="Питомец", look=look)
    save_pet(user_id, pet)
    return pet

def get_or_create_pet(user_id: int):
    pet = get_pet(user_id)
    if pet is None:
        pet = create_pet(user_id)
    return pet

def delete_pet(user_id: int):
    db.remove(User.user_id == user_id)
