from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from TelegramAPI.config import config

bot = TeleBot(config.TOKEN_API, parse_mode='html')

def get_name_keyboard():
	keyboard = InlineKeyboardMarkup()
	true = InlineKeyboardButton('Да✔️', callback_data='name_true')
	false = InlineKeyboardButton('Нет✖️', callback_data='name_false')
	keyboard.add(true, false)
	return keyboard

def get_surname_keyboard():
	keyboard = InlineKeyboardMarkup()
	true = InlineKeyboardButton('Да✔️', callback_data='surname_true')
	false = InlineKeyboardButton('Нет✖️', callback_data='surname_false')
	keyboard.add(true, false)
	return keyboard

def get_direction_keyboard():
	keyboard = InlineKeyboardMarkup()
	developer = InlineKeyboardButton('🧑‍💻Разработка', callback_data='user_dir_developer')
	designer = InlineKeyboardButton('🏞Дизайн', callback_data='user_dir_designer')
	modeler = InlineKeyboardButton('⚒️Моделирование', callback_data='user_dir_modeler')
	keyboard.add(developer, designer, modeler)
	return keyboard

def finish_registration():
	keyboard = InlineKeyboardMarkup()
	finish = InlineKeyboardButton('Завершить🏁', callback_data='finish_registration')
	keyboard.add(finish)
	return keyboard