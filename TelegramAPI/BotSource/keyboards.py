from telebot import types
from telebot.types import InlineKeyboardMarkup


def backup_keyboard():
	back_keyboard = InlineKeyboardMarkup()
	backup_key = types.InlineKeyboardButton(text='Назад', callback_data='backup_button')
	back_keyboard.add(backup_key)
	return backup_key

def start_bot_keyboard():
	choose_role_keyboard = InlineKeyboardMarkup()
	user = types.InlineKeyboardButton('Пользователь', callback_data='user')
	admin = types.InlineKeyboardButton('Админ', callback_data='superuser')
	choose_role_keyboard.add(user, admin)
	return choose_role_keyboard
