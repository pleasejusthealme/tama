import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN not found!")

DB_PATH = "db.json"
MAX_HUNGER = 5
MAX_HAPPINESS = 5


