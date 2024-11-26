from telebot import TeleBot
from telebot import types
import sqlite3

from telebot.types import InlineKeyboardMarkup

from TelegramAPI.config.config import TOKEN_API

bot = TeleBot(TOKEN_API)

conn = sqlite3.connect('storage.db')
cursor = conn.cursor()

def choose_project():
	markup = InlineKeyboardMarkup()

	conn.execute('SELECT project_name FROM projects')
	projects = cursor.fetchall()

	buttons = [types.InlineKeyboardButton(text=project_name[0], callback_data=project_name[0]) for project_name in projects]
	for button in buttons:
		markup.add(button)
	return markup

def choose_direction(message):
	direction_buttons = InlineKeyboardMarkup()
	design = types.InlineKeyboardButton(message.chat.id, text='Дизайн', callback_data='designer')
	modeling = types.InlineKeyboardButton(message.chat.id, text='Моделирование', callback_data='modeler')
	development = types.InlineKeyboardButton(message.chat.id, text='Разработка', callback_data='developer')
	direction_buttons.add(design, modeling, development)

def create_task(call):
	chat_id = call.message.chat.id
	user_message = call.message.text
	task_number = 'Задание '
	bot.send_message(chat_id, text='Напишите задание')

	cursor.execute('SELECT MAX(id) FROM tasks')
	result = cursor.fetchone()
	next_id = (result[0] or 0) + 1
	task_number = f'task{next_id}'

	cursor.execute('INSERT INTO tasks (task_number, task_message) VALUES (?, ?)', (task_number, user_message))
	conn.commit()
	if cursor.lastrowid:
		bot.send_message(chat_id, text='Задание успешно добавлено')
	else:
		bot.send_message(chat_id, text='Не удалось связаться с БД')

	conn.close()
	return task_number