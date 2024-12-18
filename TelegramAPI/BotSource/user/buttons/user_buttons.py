from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from TelegramAPI.config import config
import sqlite3
from TelegramAPI.BotSource.user.functions import user_function, user_tasks_function

bot = TeleBot(config.TOKEN_API, parse_mode='html')

def user_keyboard():
	user_panel = InlineKeyboardMarkup()
	tasks = InlineKeyboardButton(text='📕Задания', callback_data='user_tasks')
	profile = InlineKeyboardButton(text='👤Профиль', callback_data='user_profile')
	user_panel.add(tasks,profile)
	return user_panel

def user_tasks_panel_keyboard(message):
	chat_id = message.chat.id
	view_tasks_keyboard = InlineKeyboardMarkup()
	backup = types.InlineKeyboardButton('Назад', callback_data='backup_user_task_list')
	try:
		conn1 = sqlite3.connect(config.USERS_PATH)
		cursor1 = conn1.cursor()
		cursor1.execute(
			'SELECT direction FROM users WHERE id=?',
			(chat_id,)
		)
		dir_text = cursor1.fetchone()[0]
		dir = dir_text.split('_')[-1]
		conn = sqlite3.connect(config.ADMIN_TASKS_PATH)
		cursor = conn.cursor()
		cursor.execute(
			'SELECT direction FROM tasks WHERE direction = ?',
			(dir,)
		)
		direction_text = cursor.fetchone()[0]
		project = user_tasks_function.chose_project[chat_id]['project']
		cursor.execute(
			'SELECT task_number FROM tasks WHERE claim_project = ? AND direction = ?',
            (project, direction_text)
		)
		tasks = cursor.fetchall()
		print(tasks)

		buttons = [
			types.InlineKeyboardButton(
				text=f'Задание {task_number[0]}',
				callback_data=f'u_task_{task_number[0]}'
			)
			for task_number in tasks
		]

		for button in buttons:
			view_tasks_keyboard.add(button)
		view_tasks_keyboard.add(backup)
		return view_tasks_keyboard
		conn.close()
		conn1.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		user_function.user_panel(message)
