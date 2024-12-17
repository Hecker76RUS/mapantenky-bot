from telebot import TeleBot
import sqlite3

from telebot import types
from telebot.types import InlineKeyboardMarkup
from TelegramAPI.config.config import TOKEN_API, PROJECTS_PATH
from TelegramAPI.config import config
from TelegramAPI.config.config import TOKEN_API, ADMIN_TASKS_PATH


bot = TeleBot(TOKEN_API)

def choose_project_keyboard(message):
	chat_id = message.chat.id
	chose_project_keyboard = InlineKeyboardMarkup()
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
			chose_project_keyboard.add(button)
		chose_project_keyboard.add(backup)
		return chose_project_keyboard
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')

def choose_direction():
	direction_buttons = InlineKeyboardMarkup()
	design = types.InlineKeyboardButton(text='Дизайн', callback_data='dir_designer')
	modeling = types.InlineKeyboardButton(text='Моделирование', callback_data='dir_modeler')
	development = types.InlineKeyboardButton(text='Разработка', callback_data='dir_developer')
	backup = types.InlineKeyboardButton(text='Назад', callback_data='backup_tasks_choose_direction_button')
	direction_buttons.add(design, modeling, development, backup)
	return direction_buttons

def select_tasks_keyboard(message):
	chat_id = message.chat.id
	choose_tasks_keyboard = InlineKeyboardMarkup()
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
			choose_tasks_keyboard.add(button)
		choose_tasks_keyboard.add(backup)
		return choose_tasks_keyboard
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		is_projects_open(message)


