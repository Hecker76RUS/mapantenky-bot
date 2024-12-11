from TelegramAPI.BotSource.admin.buttons.admin_buttons import projects_keyboard
from TelegramAPI.config.config import TOKEN_API
from telebot import TeleBot
import sqlite3

bot = TeleBot(TOKEN_API)

def is_projects_open(call):
	chat_id = call.message.chat.id
	bot.send_message(chat_id, text='Выберите действие:', reply_markup=projects_keyboard())
	return projects_keyboard()

@bot.message_handler(func=lambda message: True)
def add_new_project(call):
	chat_id = call.message.chat.id
	bot.send_message(chat_id, text='Введите название проекта:')
	def check_project_name(message):
		project_name = message.text.strip().lower()
		conn = sqlite3.connect('tasks.db')
		cursor = conn.cursor()

		# Check if project exists
		cursor.execute("SELECT 1 FROM projects WHERE LOWER(project_name) = ?", (project_name,))
		data = cursor.fetchone()

		if data:
			bot.send_message(chat_id, text='Проект с таким названием уже существует.')
		else:
			# Insert the new project
			cursor.execute("INSERT INTO projects (project_name) VALUES (?)", (message.text,))
			conn.commit()
			bot.send_message(chat_id, text='Проект успешно добавлен в базу данных.')

		cursor.close()
		conn.close()

	bot.register_next_step_handler_by_chat_id(chat_id, check_project_name)