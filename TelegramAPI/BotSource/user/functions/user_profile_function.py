from telebot import TeleBot
import sqlite3
from TelegramAPI.config import config
from TelegramAPI.BotSource.user.buttons import  user_profile_buttons

data_list = { }
bot = TeleBot(config.TOKEN_API, parse_mode='html')

def user_profile(message):
	chat_id = message.chat.id
	bot.send_message(chat_id, f'<b>Профиль</b>\n\n'
	                          f'👤<b>{claim_surname(message)} {claim_name(message)}</b>\n'
	                          f'<b>{claim_direction(message)}</b>\n'
	                          f'📎<b>{claim_role(message)}</b>\n\n'
	                          f'📕Задание: <b>{claim_task_activity(message)}</b>\n'
	                          f'{claim_task(message)}', reply_markup=user_profile_buttons.user_profile_keyboard(message))

def claim_name(message):
	chat_id = message.chat.id
	name = ''
	try:
		conn = sqlite3.connect(config.USERS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT name FROM users WHERE id=?', (chat_id,))
		name = cursor.fetchone()[0]
	except sqlite3.OperationalError as e:
		print(e)
	finally:
		if conn:
			conn.close()
		return name

def claim_surname(message):
	chat_id = message.chat.id
	surname = ''
	try:
		conn = sqlite3.connect(config.USERS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT surname FROM users WHERE id=?', (chat_id,))
		surname = cursor.fetchone()[0]
	except sqlite3.OperationalError as e:
		print(e)
	finally:
		if conn:
			conn.close()
		return surname

def claim_direction(message):
	chat_id = message.chat.id
	direction = ''
	try:
		conn = sqlite3.connect(config.USERS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT direction FROM users WHERE id=?', (chat_id,))
		a = cursor.fetchone()[0]
		dir = a.split('_')[-1]
		if dir == 'developer':
			direction = '🧑‍💻Разработка'
		elif dir == 'modeler':
			direction = '⚒️Моделирование'
		elif dir == 'designer':
			direction = '🏞Дизайн'
	except sqlite3.OperationalError as e:
		print(e)
	finally:
		if conn:
			conn.close()
		return direction

def claim_role(message):
	chat_id = message.chat.id
	role = ''
	try:
		conn = sqlite3.connect(config.USERS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT role FROM users WHERE id=?', (chat_id,))
		role = cursor.fetchone()[0]
		if role == 'superuser':
			role = 'Администратор'
		else:
			role = 'Пользователь'
	except sqlite3.OperationalError as e:
		print(e)
	finally:
		if conn:
			conn.close()
		return role

def claim_task_activity(message):
	chat_id = message.chat.id
	activity = ''
	try:
		conn = sqlite3.connect(config.USERS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT active_task FROM users WHERE id=?', (chat_id,))
		act = cursor.fetchone()[0]
		if act != '1':
			activity = 'Есть'
		else:
			activity = 'Нет'
	except sqlite3.OperationalError as e:
		print(e)
	finally:
		if conn:
			conn.close()
		return activity

def claim_task(message):
	chat_id = message.chat.id
	try:
		conn = sqlite3.connect(config.USERS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT task FROM users WHERE id=?', (chat_id,))
		task = cursor.fetchone()[0]
		print(task)
		if task != None:
			return task

	except sqlite3.OperationalError as e:
		print(e)
	finally:
		if conn:
			conn.close()

def task_complete(message):
	chat_id = message.chat.id
	try:
		# Берем данные из строки пользователя
		print(chat_id)
		conn = sqlite3.connect(config.USERS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT name FROM users WHERE id=?', (chat_id,))
		name = str(cursor.fetchone()[0])
		print(name)

		cursor.execute('SELECT surname FROM users WHERE id=?', (chat_id,))
		surname = str(cursor.fetchone()[0])
		print(surname)

		cursor.execute('SELECT task FROM users WHERE id=?', (chat_id,))
		task = str(cursor.fetchone()[0])
		print(task)

		# Изменяю таск сообщение на null
		cursor.execute('UPDATE users SET task=? WHERE id=?', (None, chat_id))
		# Заносим данные о завершении в таблиции
		cursor.execute(
			'INSERT INTO completed_tasks (id, name, surname, task) VALUES (?,?,?,?)',
			(chat_id, name, surname, task)
		)
		conn.commit()
		conn2 = sqlite3.connect(config.ADMIN_TASKS_PATH)
		cursor2 = conn2.cursor()
		cursor2.execute('DELETE FROM tasks WHERE task_message=?', (task,))
		conn2.commit()
		bot.send_message(chat_id, f'<b>{name}</b>, вы завершили задание')
		user_profile(message)
	except sqlite3.OperationalError as e:
			print(e)
	finally:
		if conn:
			conn.close()
		if conn2:
			conn2.close()

def on_click_change_dir(call):
	chat_id = call.message.chat.id
	bot.send_message(chat_id, 'Выберите направление, в котором вы хотите работать:',reply_markup=user_profile_buttons.change_direction_keyboard(call.message) )
def change_direction(call):
	chat_id = call.message.chat.id
	callback_d = call.data
	print(callback_d)
	callback_data = callback_d.split('_', 1)[1]
	print(callback_data)
	try:
		conn = sqlite3.connect(config.USERS_PATH)
		cursor = conn.cursor()
		cursor.execute('UPDATE users SET change_direction=? WHERE id=?', (callback_d, chat_id))
		cursor.execute('UPDATE users SET direction=? WHERE id=?', (callback_data, chat_id))
		conn.commit()
		bot.send_message(chat_id, 'Вы успешно сменили направление')
		user_profile(call.message)
	except sqlite3.OperationalError as e:
		print(e)
	finally:
		if conn:
			conn.close()


