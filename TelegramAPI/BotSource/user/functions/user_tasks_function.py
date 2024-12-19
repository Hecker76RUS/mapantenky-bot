from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from TelegramAPI.config import config
import sqlite3
from TelegramAPI.BotSource.admin.functions import tasks_function
from TelegramAPI.BotSource.user.buttons import user_buttons, user_tasks_buttons
from TelegramAPI.BotSource.user.functions import user_function

bot = TeleBot(config.TOKEN_API, parse_mode='html')
chose_project = {}

def choose_user_project(message):
	chat_id = message.chat.id
	bot.send_message(chat_id, 'Выберите проект:', reply_markup=user_tasks_buttons.choose_user_project_keyboard(message))

def user_tasks_panel(call):
	chat_id = call.message.chat.id
	callback = call.data
	chose_project[chat_id] = chose_project.get(chat_id, { })
	chose_project[chat_id]['project'] = callback
	bot.send_message(chat_id, '<b>Список доступных заданий:</b>', reply_markup=user_buttons.user_tasks_panel_keyboard(call.message))

def show_user_task(call):
	callback_data = call.data
	chat_id = call.message.chat.id
	tasks_list_keyboard = types.InlineKeyboardMarkup()
	try:
		conn = sqlite3.connect(config.ADMIN_TASKS_PATH)
		cursor = conn.cursor()
		cursor.execute('SELECT task_message FROM tasks WHERE user_task = ?',
		               (callback_data,))
		text = cursor.fetchone()[0]
		claim = InlineKeyboardButton(text='Взять', callback_data=f'claim_{callback_data}')
		backup_button = InlineKeyboardButton(text='Назад', callback_data='backup_user_show_tasks')
		tasks_list_keyboard.add(claim, backup_button)
		bot.send_message(chat_id, f'<b>Задание выглядит так:</b> \n{text}', reply_markup=tasks_list_keyboard)
		conn.close()
	except sqlite3.Error as e:
		bot.send_message(chat_id, f'Ошибка при работе с базой данных: {e}')
		tasks_function.select_tasks(call.message)
		conn.close()

def claim_task(call):
	callback_data = call.data
	chat_id = call.message.chat.id
	conn1 = None
	conn2 = None

	try:
		conn1 = sqlite3.connect(config.ADMIN_TASKS_PATH)
		cursor1 = conn1.cursor()
		conn2 = sqlite3.connect(config.USERS_PATH)
		cursor2 = conn2.cursor()

		cursor1.execute(
			'SELECT task_message FROM tasks WHERE claim_user_task = ?',
			(callback_data,)
		)
		result1 = cursor1.fetchone()
		print(result1)
		cursor2.execute(
			'SELECT task FROM users WHERE id = ?',
			(chat_id,)
		)
		task_info = cursor2.fetchone()[0]
		print(task_info)

		if result1:
			text = result1[0]
			print(f'text:{text}')
		else:
			bot.send_message(chat_id, 'Задание не найдено.')
			return

		cursor1.execute(
			'SELECT task_number FROM tasks WHERE claim_user_task = ?',
			(callback_data,)
		)
		result2 = cursor1.fetchone()
		print(result2)
		if result2:
			num = result2[0]
		else:
			bot.send_message(chat_id, 'Задание не найдено.')
			return
		project = chose_project[chat_id]['project']
		if task_info == None:
			cursor2.execute(
				'UPDATE users SET project = ? WHERE id = ?',
				(project, chat_id)
			)
			cursor2.execute(
				'UPDATE users SET task = ? WHERE id = ?',
				(text, chat_id)
			)
			cursor2.execute(
				'UPDATE users SET active_task = ? WHERE id = ?',
				(num, chat_id)
			)
			conn2.commit()
			bot.send_message(chat_id, 'Задание успешно взято \nИнформация о задании находится во '
		                          'вкладке 👤<b>Профиль</b>')
			user_function.user_panel(call.message)
		else:
			bot.send_message(chat_id, 'Вы уже взяли задание.\n Закончите его, чтобы приступить к следующему')
			user_function.user_panel(call.message)
	except sqlite3.Error as e:
		print(f'{e}')
	finally:
		if conn1:
			conn1.close()
		if conn2:
			conn2.close()