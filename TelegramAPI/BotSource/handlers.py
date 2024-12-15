from telebot.types import InlineKeyboardMarkup
from telebot import TeleBot
from telebot import types
from TelegramAPI.config.config import TOKEN_API
from TelegramAPI.BotSource.admin.functions import projects_function, profile_function, tasks_function
from TelegramAPI.BotSource.admin.buttons.admin_buttons import admin_keyboard, connect_checker
from TelegramAPI.BotSource.admin.buttons import tasks_buttons
from TelegramAPI.BotSource.keyboards import backup_keyboard, start_bot_keyboard
bot = TeleBot(TOKEN_API, parse_mode='html')