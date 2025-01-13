import sqlite3

from telebot import TeleBot
from telebot import types
from telebot.types import InlineKeyboardMarkup

from TelegramAPI.BotSource.admin.functions.projects_function import if_projects_open
from config.config import TOKEN_API, PROJECTS_PATH, ADMIN_TASKS_PATH
from config import config

bot = TeleBot(TOKEN_API)

def choose_project_keyboard(message):
	chat_id = message.chat.id
	markup = InlineKeyboardMarkup()
	backup = types.InlineKeyboardButton('Назад', callback_data='backup_task_choose_project_button')
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
			markup.add(button)
		markup.add(backup)
		return markup
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
	finally:
		if conn:
			conn.close()

def choose_direction():
	markup = InlineKeyboardMarkup()
	design = types.InlineKeyboardButton(text='Дизайн', callback_data='dir_designer')
	modeling = types.InlineKeyboardButton(text='Моделирование', callback_data='dir_modeler')
	development = types.InlineKeyboardButton(text='Разработка', callback_data='dir_developer')
	backup = types.InlineKeyboardButton(text='Назад', callback_data='backup_tasks_choose_direction_button')
	markup.add(design, modeling, development, backup)
	return markup

def select_tasks_keyboard(message):
	chat_id = message.chat.id
	markup = InlineKeyboardMarkup()
	backup = types.InlineKeyboardButton('Назад', callback_data='backup_task_select_button')
	try:
		conn = sqlite3.connect(ADMIN_TASKS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT task_id FROM tasks')
		tasks = cursor.fetchall()

		buttons = [
			types.InlineKeyboardButton(
				text=f'Задание {task_id[0]}',
				callback_data=f'check_{task_id[0]}'
			)
			for task_id in tasks
		]

		for button in buttons:
			markup.add(button)
		markup.add(backup)
		return markup
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		if_projects_open(message)
	finally:
		if conn:
			conn.close()


