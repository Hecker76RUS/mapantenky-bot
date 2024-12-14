import sqlite3

from telebot import TeleBot
from TelegramAPI.BotSource.admin.buttons import admin_buttons
from TelegramAPI.config.config import TOKEN_API

bot = TeleBot(TOKEN_API)

def is_tasks_open(call):
	chat_id = call.message.chat.id
	bot.send_message(chat_id, 'Выберите действие:', reply_markup=admin_buttons.tasks_keyboard())

def create_task(message):
	chat_id = message.chat.id
	user_message = message.text
	try:
		conn = sqlite3.connect('C:\\Users\\kudrii\\PycharmProjects\\Mapantenky_bot\\TelegramAPI\\DataBases\\admin_tasks.db')
		cursor = conn.cursor()

		cursor.execute('SELECT MAX(task_id) FROM tasks')
		result = cursor.fetchone()
		next_id = (result[0] or 0) + 1 if result else 1

		task_number = next_id

		cursor.execute(
		    'INSERT INTO tasks (task_id, task_message) VALUES (?, ?)',
		    (task_number, user_message)
		)
		conn.commit()

		if cursor.lastrowid:
			bot.send_message(chat_id, text='Задание успешно добавлено')
		else:
			bot.send_message(chat_id, text='Не удалось добавить задание в БД')

	except sqlite3.Error as e:
		bot.send_message(chat_id, text=f'Ошибка работы с базой данных: {e}')
	finally:
		conn.close()