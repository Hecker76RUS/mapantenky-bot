import sqlite3

from telebot import TeleBot
from telebot import types
from telebot.types import InlineKeyboardMarkup
from TelegramAPI.BotSource.admin.buttons import admin_buttons, tasks_buttons
from TelegramAPI.config.config import TOKEN_API, ADMIN_TASKS_PATH
from TelegramAPI.config import config
from TelegramAPI.BotSource.admin.functions.projects_function import if_projects_open

bot = TeleBot(TOKEN_API)
user_data = {}

def choose_project(message):
	chat_id = message.chat.id
	photo_path = config.CREATE_TASK
	with open(photo_path, "rb") as photo:
		bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=tasks_buttons.choose_project_keyboard(message))

def if_tasks_open(message):
	chat_id = message.chat.id
	photo_path = config.TASKS
	with open(photo_path, "rb") as photo:
		bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=admin_buttons.tasks_keyboard())

def tasks_list(message):
	chat_id = message.chat.id
	markup = InlineKeyboardMarkup()
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
			markup.add(button)
		markup.add(backup)
		return markup
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		if_projects_open(message)

def active_tasks_list(message):
	chat_id = message.chat.id
	bot.send_message(chat_id, 'Активные задания', reply_markup=admin_buttons.active_tasks_list_keyboard(message))

def if_tasks_list_open(call):
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
		select_tasks_panel(call.message)
		conn.close()

def create_task(message):
	chat_id = message.chat.id
	user_message = message.text
	dir_code = ''
	try:
		conn = sqlite3.connect(ADMIN_TASKS_PATH)
		cursor = conn.cursor()

		cursor.execute('SELECT MAX(task_number) FROM tasks')
		result = cursor.fetchone()
		next_id = (result[0] or 0) + 1 if result else 1
		task_number = next_id
		project_name = user_data.get(chat_id, {}).get('project', 'Не указан')
		direction = user_data.get(chat_id, { }).get('direction', 'Не указано')

		if direction == 'developer':
			dir_code = '01'
		if direction == 'modeler':
			dir_code = '02'
		if direction == 'designer':
			dir_code = '03'

		user_data[chat_id]['dir_code'] = dir_code

		dir_code = user_data.get(chat_id, {}).get('dir_code')
		task_id = f'task_{next_id}'
		task_code = f'{dir_code}{next_id}'

		cursor.execute(
			'INSERT INTO tasks (task_number,task_id, check_task, delete_task, project, direction, task_message, user_task, claim_user_task, claim_project) VALUES (?,?,?,?,?,?,?,?,?,?)',
			(task_number, task_id, f'check_task_{task_number}',f'delete_check_task_{task_number}',
			 project_name, direction, f'№:{task_code}\n\n<b>Задание:</b>\n{user_message}', f'u_task_{task_number}', f'claim_u_task_{task_number}', f'users_project_{project_name}')
		)
		conn.commit()

		if cursor.lastrowid:
			bot.send_message(chat_id, text='Задание успешно добавлено')
			if_tasks_open(message)

		else:
			bot.send_message(chat_id, text='Не удалось добавить задание в БД')
			if_tasks_open(message)

	except sqlite3.Error as e:
		bot.send_message(chat_id, text=f'Ошибка работы с базой данных: {e}')
		if_tasks_open(message)
	finally:
		conn.close()

def select_tasks_panel(message):
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
		select_tasks_panel(call.message)
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
			if_tasks_open(call.message)
		else:
			bot.send_message(chat_id, f"Задание {callback_data} не найдено")
		conn.close()

	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		if_tasks_open(call.message)
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
