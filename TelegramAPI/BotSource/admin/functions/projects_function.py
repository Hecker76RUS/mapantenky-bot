from TelegramAPI.BotSource.admin.buttons.admin_buttons import projects_keyboard
from TelegramAPI.config.config import TOKEN_API
from telebot import TeleBot
import sqlite3

bot = TeleBot(TOKEN_API)

def is_projects_open(message):
	chat_id = message.chat.id
	bot.send_message(chat_id, text='Выберите действие:', reply_markup=projects_keyboard())
	return projects_keyboard()

def add_new_project(message):
	chat_id = message.chat.id
	project_name = message.text.strip().lower()
	try:
		conn = sqlite3.connect('C:\\Users\\kudrii\\PycharmProjects\\Mapantenky_bot\\TelegramAPI\\DataBases\\projects.db')
		cursor = conn.cursor()

		cursor.execute("SELECT * FROM projects WHERE LOWER(project_name) = ?", (project_name,))
		data = cursor.fetchone()
		if data:
			bot.send_message(chat_id, text='Проект с таким названием уже существует.')
			conn.close()
		else:
			cursor.execute(
				"INSERT INTO projects (project_name, project_name_callback) VALUES (?,?)",
			    (message.text, message.text)
			)
			conn.commit()
			conn.close()
			bot.send_message(chat_id, text='Проект успешно добавлен в базу данных.')

	except Exception as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
	finally:
		conn.close()
