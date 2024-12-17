from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from TelegramAPI.config import config

bot = TeleBot(config.TOKEN_API, parse_mode='html')