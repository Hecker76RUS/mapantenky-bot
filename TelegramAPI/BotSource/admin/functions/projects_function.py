from TelegramAPI.BotSource.admin.buttons.admin_buttons import projects_keyboard
from TelegramAPI.config.config import TOKEN_API, PROJECTS_PATH
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup
from telebot import types
import sqlite3

bot = TeleBot(TOKEN_API)

def is_projects_open(message):
	chat_id = message.chat.id
	bot.send_message(chat_id, text='Выберите действие:', reply_markup=projects_keyboard())
	return projects_keyboard()

def add_new_project(message):
	chat_id = message.chat.id
	project_name = message.text.strip().lower()
	try:
		conn = sqlite3.connect(PROJECTS_PATH)
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
			is_projects_open(message)
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		is_projects_open(message)
	finally:
		conn.close()

def select_project(message):
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
				callback_data=f'delete_project_{project_name[0]}'
			)
			for project_name in projects
		]

		for button in buttons:
			choose_project_keyboard.add(button)
		return choose_project_keyboard
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		is_projects_open(message)

def delete_project(call):
	callback_data = call.data
	chat_id = call.message.chat.id

	try:
		conn = sqlite3.connect(PROJECTS_PATH)
		cursor = conn.cursor()

		cursor.execute('DELETE FROM projects WHERE delete_project = ?', (callback_data,))
		conn.commit()
		if cursor.rowcount > 0:
			bot.send_message(chat_id, f"Проект {callback_data} был удален")
			is_projects_open(call.message)
		else:
			bot.send_message(chat_id, f"Проект {callback_data} не найден")
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		is_projects_open(call.message)
		conn.close()