import sqlite3
import time

from telebot import TeleBot
from telebot import types
from telebot.types import InlineKeyboardMarkup
from TelegramAPI.BotSource.admin.buttons import admin_buttons
from TelegramAPI.config.config import TOKEN_API, ADMIN_TASKS_PATH
from TelegramAPI.BotSource.admin.buttons import tasks_buttons

bot = TeleBot(TOKEN_API)

def is_tasks_open(message):
	chat_id = message.chat.id
	bot.send_message(chat_id, 'Выберите действие:', reply_markup=admin_buttons.tasks_keyboard())

def tasks_list(message):
	chat_id = message.chat.id
	view_tasks_keyboard = InlineKeyboardMarkup()
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
		backup_button = types.InlineKeyboardButton(text='Назад', callback_data='backup_delete_tasks_button')
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
		task_id = f'task_{next_id}'

		cursor.execute(
		    'INSERT INTO tasks (task_number,task_id, check_task, delete_task, task_message) VALUES (?,?,?,?,?)',
		    (task_number, task_id, f'check_task_{task_number}',f'delete_check_task_{task_number}', user_message)
		)
		conn.commit()

		if cursor.lastrowid:
			print(f'Данные добавлены в таблицу tasks. Добавленные данные: {task_number}, {user_message}')
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
	choose_tasks_keyboard = InlineKeyboardMarkup()
	try:
		conn = sqlite3.connect(ADMIN_TASKS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT task_number FROM tasks')
		tasks = cursor.fetchall()

		buttons = [
			types.InlineKeyboardButton(
				text=f'Задание {task_number[0]}',
				callback_data=f'check_task_{task_number[0]}'
			)
			for task_id in tasks
		]

		for button in buttons:
			choose_tasks_keyboard.add(button)
		return choose_tasks_keyboard
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		is_projects_open(message)

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