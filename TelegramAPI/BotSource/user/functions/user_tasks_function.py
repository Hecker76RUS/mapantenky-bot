from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from TelegramAPI.config import config
import sqlite3
from TelegramAPI.BotSource.admin.functions import tasks_function

bot = TeleBot(config.TOKEN_API, parse_mode='html')

def user_tasks_panel(message):
	chat_id = message.chat.id
	view_tasks_keyboard = InlineKeyboardMarkup()
	backup = types.InlineKeyboardButton('Назад', callback_data='backup_user_task_list')
	try:
		conn = sqlite3.connect(config.ADMIN_TASKS_PATH)
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

def show_user_task(call):
	callback_data = call.data
	chat_id = call.message.chat.id
	tasks_list_keyboard = types.InlineKeyboardMarkup()
	try:
		conn = sqlite3.connect(config.ADMIN_TASKS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT task_message FROM tasks WHERE task_id = ?',
		               (callback_data,))
		text = cursor.fetchone()[0]
		backup_button = types.InlineKeyboardButton(text='Назад', callback_data='backup_user_show_tasks')
		tasks_list_keyboard.add(backup_button)
		bot.send_message(chat_id, f'Задание выглядит так:{text}', reply_markup=tasks_list_keyboard)
		conn.close()
	except sqlite3.Error as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		tasks_function.select_tasks(call.message)
		conn.close()