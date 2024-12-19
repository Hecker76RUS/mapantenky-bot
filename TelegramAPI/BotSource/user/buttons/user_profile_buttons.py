from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from TelegramAPI.config import config

bot = TeleBot(config.TOKEN_API, parse_mode='html')

def user_profile_keyboard(message):
	keyboard = InlineKeyboardMarkup()
	change_direction = InlineKeyboardButton(text='Сменить направление🔄', callback_data='change_direction')
	keyboard.add(change_direction)
	complete_task = InlineKeyboardButton(text='Завершить задание✅', callback_data='task_complete')
	keyboard.add(complete_task)
	backup = InlineKeyboardButton(text='🔙Назад', callback_data='user_backup_profile_button')
	keyboard.add(backup)
	return keyboard

def change_direction_keyboard(message):
	keyboard = InlineKeyboardMarkup()
	developer = InlineKeyboardButton('🧑‍💻Разработка', callback_data='change_user_dir_developer')
	designer = InlineKeyboardButton('🏞Дизайн', callback_data='change_user_dir_designer')
	modeler = InlineKeyboardButton('⚒️Моделирование', callback_data='change_user_dir_modeler')
	keyboard.add(developer, designer, modeler)
	return keyboard