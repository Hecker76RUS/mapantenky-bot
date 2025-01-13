from TelegramAPI.BotSource.admin.buttons.admin_buttons import projects_keyboard
from TelegramAPI.config.config import TOKEN_API, PROJECTS_PATH
from TelegramAPI.config import config
from TelegramAPI.BotSource.admin.buttons import  projects_buttons
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup
from telebot import types
import sqlite3

bot = TeleBot(TOKEN_API)

def if_projects_open(message):
	chat_id = message.chat.id
	photo_path = config.PROJECTS
	with open(photo_path, "rb") as photo:
		bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=projects_keyboard())
	return projects_keyboard()

def add_new_project(message):
	chat_id = message.chat.id
	photo_path = config.CREATE_PROJECT
	with open(photo_path, "rb") as photo:
		bot.send_photo(chat_id=chat_id, photo=photo, caption='Введите название проекта:')

def select_project(message):
	chat_id = message.chat.id
	photo_path = config.DELETE_PROJECT
	with open(photo_path, "rb") as photo:
		bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=projects_buttons.select_project_keyboard(message))

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
			if_projects_open(call.message)
		else:
			bot.send_message(chat_id, f"Проект {callback_data} не найден")
		conn.close()
	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		if_projects_open(call.message)
		conn.close()