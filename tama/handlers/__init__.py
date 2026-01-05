from aiogram import Dispatcher
from .start import register_start_handlers
from .game import register_game_handlers

def register_handlers(dp: Dispatcher):
    register_start_handlers(dp)
    register_game_handlers(dp)
