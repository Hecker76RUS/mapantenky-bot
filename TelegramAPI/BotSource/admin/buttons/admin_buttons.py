import sqlite3
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup

from TelegramAPI.config.config import TOKEN_API, ADMIN_TASKS_PATH, PROJECTS_PATH, USERS_PATH

bot = telebot.TeleBot(TOKEN_API)
# Таски, проекты, профиль. Основная страница
def admin_keyboard():
	admin_panel = InlineKeyboardMarkup()
	tasks_button = types.InlineKeyboardButton(text='Задания', callback_data='admin_tasks')
	project_button = types.InlineKeyboardButton(text='Проекты', callback_data='admin_projects')
	check_connection = types.InlineKeyboardButton(text='Подключение', callback_data='check_connect')
	profile_button = types.InlineKeyboardButton(text='Профиль', callback_data='admin_profile')
	task_list = types.InlineKeyboardButton(text='Активные задания', callback_data='active_tasks')
	admin_panel.add(tasks_button, project_button, check_connection, profile_button, task_list)
	return admin_panel

def tasks_keyboard():
	tasks_panel = InlineKeyboardMarkup()
	create_task = types.InlineKeyboardButton(text='Добавить задание', callback_data='create_task')
	delete_task = types.InlineKeyboardButton(text='Удалить задание', callback_data='delete_task')
	tasks_list = types.InlineKeyboardButton(text='Список заданий', callback_data='tasks_list')
	backup_key = types.InlineKeyboardButton(text='Назад', callback_data='admin_tasks_backup_button')
	tasks_panel.add(create_task, delete_task, backup_key, tasks_list)
	return tasks_panel

def projects_keyboard():
	projects_panel = InlineKeyboardMarkup()
	create_project = types.InlineKeyboardButton(text='Добавить проект', callback_data='create_project')
	delete_project = types.InlineKeyboardButton(text='Удалить проект', callback_data='delete_project')
	projects_list = types.InlineKeyboardButton(text='Список проектов', callback_data='projects_list')
	backup_key = types.InlineKeyboardButton(text='Назад', callback_data='admin_projects_backup_button')
	projects_panel.add(create_project, delete_project, backup_key, projects_list)
	return projects_panel

def profile_keyboard():
	profile_panel = InlineKeyboardMarkup()
	ssh_key = types.InlineKeyboardButton(text='SSH-Key', callback_data='ssh_key')
	backup_key = types.InlineKeyboardButton(text='Назад', callback_data='admin_profile_backup_button')
	profile_panel.add(ssh_key, backup_key)
	return profile_panel

def active_profile_keyboard():
	profile_panel = InlineKeyboardMarkup()
	backup_key = types.InlineKeyboardButton(text='Назад', callback_data='admin_active_profile_backup_button')
	profile_panel.add(backup_key)
	return profile_panel

def active_tasks_list_keyboard(message):
	chat_id = message.chat.id
	markup = InlineKeyboardMarkup()
	backup = types.InlineKeyboardButton('Назад', callback_data='backup_task_list_button')
	try:
		conn = sqlite3.connect(USERS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT active_task FROM users WHERE task is not null')
		tasks = cursor.fetchall()
		print('успешное подключение к бд users.db')

		buttons = [
			types.InlineKeyboardButton(
				text=f'{active_task[0]}',
				callback_data=f'active_{active_task[0]}'
			)
			for active_task in tasks
		]

		for button in buttons:
			markup.add(button)
		markup.add(backup)
		return markup
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		print(f'ошибка {e}')

def active_task_text(call):
	input_data = call.data
	callback_data = input_data.split('_')[1]
	print(callback_data)
	chat_id = call.message.chat.id
	tasks_list_keyboard = types.InlineKeyboardMarkup()
	try:
		conn = sqlite3.connect(USERS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT task FROM users WHERE active_task = ?',
		               (callback_data,))
		text = cursor.fetchall()
		backup_button = types.InlineKeyboardButton(text='Назад', callback_data='backup_task_select_button')
		tasks_list_keyboard.add(backup_button)
		bot.send_message(chat_id, f'Задание выглядит так:{text}', reply_markup=tasks_list_keyboard)
		conn.close()
	except sqlite3.Error as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		conn.close()

def connect_checker(call):
	try:
		conn1 = sqlite3.connect(PROJECTS_PATH)
		cursor1 = conn1.cursor()
		cursor1.execute('SELECT project_name FROM projects')
		result1 = cursor1.fetchall()
		if result1:
			bot.send_message(call.message.chat.id, 'Подключение к БД-1 стабильно')
		else:
			bot.send_message(call.message.chat.id, 'Нет подключения к БД-1 ')
		conn2 = sqlite3.connect(ADMIN_TASKS_PATH)
		cursor2 = conn2.cursor()
		cursor2.execute('SELECT task_id FROM tasks')

		result2 = cursor2.fetchall()
		if result2:
			bot.send_message(call.message.chat.id, 'Подключение к БД-2 стабильно')
		else:
			bot.send_message(call.message.chat.id, 'Нет подключения к БД-2 ')
	except sqlite3.Error as e:
		bot.send_message(call.message.chat.id, f'Ошибка подключения: {e}')
	finally:
		conn1.close()
		conn2.close()
