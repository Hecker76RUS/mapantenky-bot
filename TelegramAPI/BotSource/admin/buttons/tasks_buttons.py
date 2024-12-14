from telebot import TeleBot
import sqlite3

from telebot import types

from TelegramAPI.config.config import TOKEN_API

bot = TeleBot(TOKEN_API)

def choose_project(message):
	chat_id = message.chat.id
	choose_project_keyboard = types.InlineKeyboardMarkup()
	try:
		with sqlite3.connect('C:\\Users\\kudrii\\PycharmProjects\\Mapantenky_bot\\TelegramAPI\\DataBases\\projects.db') as conn:
			cursor = conn.cursor()
			cursor.execute('SELECT project_name FROM projects')
			projects = cursor.fetchall()

			buttons = [
				types.InlineKeyboardButton(
					text=f'{project_name[0]}',
					callback_data=f'{project_name[0]}'
				)
				for project_name in projects
			]

			for button in buttons:
				choose_project_keyboard.add(button)
		return choose_project_keyboard

	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')

def choose_direction():
	direction_buttons = types.InlineKeyboardMarkup()
	design = types.InlineKeyboardButton(text='Дизайн', callback_data='designer')
	modeling = types.InlineKeyboardButton(text='Моделирование', callback_data='modeler')
	development = types.InlineKeyboardButton(text='Разработка', callback_data='developer')
	direction_buttons.add(design, modeling, development)
