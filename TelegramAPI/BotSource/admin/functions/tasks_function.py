import sqlite3

from telebot import TeleBot
from telebot import types
from telebot.types import InlineKeyboardMarkup
from TelegramAPI.BotSource.admin.buttons import admin_buttons, tasks_buttons
from TelegramAPI.config.config import TOKEN_API, ADMIN_TASKS_PATH
from TelegramAPI.config import config

bot = TeleBot(TOKEN_API)
user_data = {}

def choose_project(message):
	chat_id = message.chat.id
	photo_path = config.CREATE_TASK
	with open(photo_path, "rb") as photo:
		bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=tasks_buttons.choose_project_keyboard(message))

def is_tasks_open(message):
	chat_id = message.chat.id
	photo_path = config.TASKS
	with open(photo_path, "rb") as photo:
		bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=admin_buttons.tasks_keyboard())

def tasks_list(message):
	chat_id = message.chat.id
	view_tasks_keyboard = InlineKeyboardMarkup()
	backup = types.InlineKeyboardButton('Назад', callback_data='backup_task_list_button')
	try:
		conn = sqlite3.connect(ADMIN_TASKS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT task_id FROM tasks')
		tasks = cursor.fetchall()

		buttons = [
			types.InlineKeyboardButton(
				text=f'{task_id[0]}',
				callback_data=f'{task_id[0]}'
			)
			for task_id in tasks
		]

		for button in buttons:
			view_tasks_keyboard.add(button)
		view_tasks_keyboard.add(backup)
		return view_tasks_keyboard
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		is_projects_open(message)

def is_tasks_list_open(call):
	callback_data = call.data
	chat_id = call.message.chat.id
	tasks_list_keyboard = types.InlineKeyboardMarkup()
	try:
		conn = sqlite3.connect(ADMIN_TASKS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT task_message FROM tasks WHERE task_id = ?',
					   (callback_data,))
		text = cursor.fetchall()
		backup_button = types.InlineKeyboardButton(text='Назад', callback_data='backup_task_select_button')
		tasks_list_keyboard.add(backup_button)
		bot.send_message(chat_id, f'Задание выглядит так:{text}', reply_markup=tasks_list_keyboard)
		conn.close()
	except sqlite3.Error as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		select_tasks(call.message)
		conn.close()

def create_task(message):
	chat_id = message.chat.id
	user_message = message.text

	try:
		conn = sqlite3.connect(ADMIN_TASKS_PATH)
		cursor = conn.cursor()

		cursor.execute('SELECT MAX(task_number) FROM tasks')
		result = cursor.fetchone()
		next_id = (result[0] or 0) + 1 if result else 1
		task_number = next_id
		project_name = user_data.get(chat_id, {}).get('project', 'Не указан')
		direction = user_data.get(chat_id, { }).get('direction', 'Не указано')
		task_id = f'task_{next_id}'

		cursor.execute(
			'INSERT INTO tasks (task_number,task_id, check_task, delete_task, project, direction, task_message) VALUES (?,?,?,?,?,?,?)',
			(task_number, task_id, f'check_task_{task_number}',f'delete_check_task_{task_number}', project_name, direction, user_message)
		)
		conn.commit()

		if cursor.lastrowid:
			bot.send_message(chat_id, text='Задание успешно добавлено')
			is_tasks_open(message)

		else:
			bot.send_message(chat_id, text='Не удалось добавить задание в БД')
			is_tasks_open(message)

	except sqlite3.Error as e:
		bot.send_message(chat_id, text=f'Ошибка работы с базой данных: {e}')
		is_tasks_open(message)
	finally:
		conn.close()

def select_tasks(message):
	chat_id = message.chat.id
	photo_path = config.DELETE_TASK
	with open(photo_path, "rb") as photo:
		bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=tasks_buttons.select_tasks_keyboard(message))

def view_selected_task(call):
	callback_data = call.data
	chat_id = call.message.chat.id
	view_tasks_keyboard = types.InlineKeyboardMarkup()
	try:
		conn = sqlite3.connect(ADMIN_TASKS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT task_message FROM tasks WHERE check_task = ?',
					   (callback_data,))
		text = cursor.fetchall()
		backup_button = types.InlineKeyboardButton(text='Назад', callback_data='backup_delete_tasks_button')
		delete_task_button = types.InlineKeyboardButton(text='Удалить', callback_data=f'delete_{callback_data}')
		view_tasks_keyboard.add(backup_button, delete_task_button)
		bot.send_message(chat_id, f'Задание выглядит так:{text}', reply_markup=view_tasks_keyboard)
		conn.close()
	except sqlite3.Error as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		select_tasks(call.message)
		conn.close()

def delete_task(call):
	callback_data = call.data
	chat_id = call.message.chat.id

	try:
		conn = sqlite3.connect(ADMIN_TASKS_PATH)
		cursor = conn.cursor()

		cursor.execute('DELETE FROM tasks WHERE delete_task = ?', (callback_data,))
		conn.commit()
		if cursor.rowcount > 0:
			bot.send_message(chat_id, f"Задание {callback_data} был удалено")
			is_tasks_open(call.message)
		else:
			bot.send_message(chat_id, f"Задание {callback_data} не найдено")
		conn.close()

	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		is_tasks_open(call.message)
		conn.close()

def save_project_data(call):
	chat_id = call.message.chat.id
	project_name = call.data.split('project_')[1]
	user_data[chat_id] = user_data.get(chat_id, { })
	user_data[chat_id]['project'] = project_name
	bot.send_message(chat_id, f'Вы выбрали проект: {project_name}')
	bot.send_message(chat_id, "Теперь выберите направление:", reply_markup=tasks_buttons.choose_direction())

def save_direction_data(call):
	chat_id = call.message.chat.id
	direction = call.data.split('dir_')[1]
	user_data[chat_id] = user_data.get(chat_id, { })
	user_data[chat_id]['direction'] = direction
	bot.send_message(chat_id, f'Вы выбрали направление: {direction}')
	bot.send_message(chat_id, "Напишите описание задачи:")
