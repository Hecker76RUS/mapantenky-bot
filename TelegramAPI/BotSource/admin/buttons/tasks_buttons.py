from telebot import TeleBot
import sqlite3

from telebot import types
from telebot.types import InlineKeyboardMarkup
from TelegramAPI.config.config import TOKEN_API, PROJECTS_PATH
from TelegramAPI.BotSource.admin.functions import tasks_function

bot = TeleBot(TOKEN_API)

def choose_project(message):
	chat_id = message.chat.id
	choose_project_keyboard = InlineKeyboardMarkup()
	try:
		conn = sqlite3.connect(PROJECTS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT project_name FROM projects')
		projects = cursor.fetchall()

		buttons = [
			types.InlineKeyboardButton(
				text=f'{project_name[0]}',
				callback_data=f'project_{project_name[0]}'
			)
			for project_name in projects
		]

		for button in buttons:
			choose_project_keyboard.add(button)
		return choose_project_keyboard
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')

def choose_direction():
	direction_buttons = InlineKeyboardMarkup()
	design = types.InlineKeyboardButton(text='Дизайн', callback_data='dir_designer')
	modeling = types.InlineKeyboardButton(text='Моделирование', callback_data='dir_modeler')
	development = types.InlineKeyboardButton(text='Разработка', callback_data='dir_developer')
	direction_buttons.add(design, modeling, development)
	return direction_buttons


