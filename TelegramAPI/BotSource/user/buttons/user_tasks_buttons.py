from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from TelegramAPI.config import config
import sqlite3

bot = TeleBot(config.TOKEN_API, parse_mode='html')

def choose_user_project_keyboard(message):
	chat_id = message.chat.id
	chose_project_keyboard = InlineKeyboardMarkup()
	backup = types.InlineKeyboardButton('Назад', callback_data='backup_user_choose_project')
	try:
		conn = sqlite3.connect(config.PROJECTS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT project_name FROM projects')
		projects = cursor.fetchall()

		buttons = [
			types.InlineKeyboardButton(
				text=f'{project_name[0]}',
				callback_data=f'users_project_{project_name[0]}'
			)
			for project_name in projects
		]

		for button in buttons:
			chose_project_keyboard.add(button)
		chose_project_keyboard.add(backup)
		return chose_project_keyboard
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')