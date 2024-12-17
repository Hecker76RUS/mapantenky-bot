from telebot import TeleBot, types
import sqlite3
from TelegramAPI.config import config
from TelegramAPI.BotSource.user.functions import user_function, register_function


bot = TeleBot(config.TOKEN_API, parse_mode='html')

def check_registration(message):
	chat_id = message.chat.id
	found = False
	x = 0
	try:
		conn = sqlite3.connect(config.USERS_PATH)
		cursor = conn.cursor()
		cursor.execute(
			'SELECT id FROM users'
		)
		len_id = cursor.fetchall()
		j = len(len_id)
		for x in range(0, j):
			user_id = len_id[x][0]
			if user_id == chat_id:
				user_function.user_panel(message)
				found = True
				break
		if not found:
			register_function.start_registration(message)

	except Exception as e:
		print(e)
	finally:
		conn.close()