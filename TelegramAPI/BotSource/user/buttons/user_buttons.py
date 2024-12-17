from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from TelegramAPI.config import config

bot = TeleBot(config.TOKEN_API, parse_mode='html')

def user_keyboard():
	user_panel = InlineKeyboardMarkup()
	tasks = InlineKeyboardButton(text='📕Задания', callback_data='user_tasks')
	profile = InlineKeyboardButton(text='👤Профиль', callback_data='user_profile')
	user_panel.add(tasks,profile)
	return user_panel

