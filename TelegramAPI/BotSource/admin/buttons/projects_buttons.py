import sqlite3
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup

from TelegramAPI.config.config import TOKEN_API
from TelegramAPI.config import config
from TelegramAPI.BotSource.admin.functions import projects_function

bot = TeleBot(TOKEN_API)



def add_new_project_keyboard(message):
	chat_id = message.chat.id
	project_name = message.text.strip().lower()
	try:
		conn = sqlite3.connect(config.PROJECTS_PATH)
		cursor = conn.cursor()

		cursor.execute("SELECT * FROM projects WHERE LOWER(project_name) = ?", (project_name,))
		data = cursor.fetchone()
		if data:
			bot.send_message(chat_id, text='Проект с таким названием уже существует.')
			conn.close()
		else:
			cursor.execute(
				"INSERT INTO projects (project_name, project_name_callback, delete_project) VALUES (?,?,?)",
			    (message.text, f'project_{message.text}', f'delete_project_{message.text}')
			)
			conn.commit()
			conn.close()
			bot.send_message(chat_id, text='Проект успешно добавлен в базу данных.')
			projects_function.is_projects_open(message)
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		projects_function.is_projects_open(message)
	finally:
		conn.close()

def projects_list(message):
	chat_id = message.chat.id
	choose_project_keyboard = InlineKeyboardMarkup()
	backup = types.InlineKeyboardButton('Назад', callback_data='backup_projects_list_button')
	try:
		conn = sqlite3.connect(config.PROJECTS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT project_name FROM projects')
		projects = cursor.fetchall()

		buttons = [
			types.InlineKeyboardButton(
				text=f'{project_name[0]}',
				callback_data=f'list_{project_name[0]}'
			)
			for project_name in projects
		]

		for button in buttons:
			choose_project_keyboard.add(button)
		choose_project_keyboard.add(backup)
		return choose_project_keyboard
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')

def select_project_keyboard(message):
	chat_id = message.chat.id
	choose_project_keyboard = InlineKeyboardMarkup()
	backup = types.InlineKeyboardButton('Назад', callback_data='backup_projects_select_button')
	try:
		conn = sqlite3.connect(config.PROJECTS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT project_name FROM projects')
		projects = cursor.fetchall()

		buttons = [
			types.InlineKeyboardButton(
				text=f'{project_name[0]}',
				callback_data=f'delete_project_{project_name[0]}'
			)
			for project_name in projects
		]

		for button in buttons:
			choose_project_keyboard.add(button)
		choose_project_keyboard.add(backup)
		return choose_project_keyboard
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		projects_function.is_projects_open(message)