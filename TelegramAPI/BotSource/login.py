from telebot.types import InlineKeyboardMarkup
from telebot import TeleBot
from telebot import types

from TelegramAPI.BotSource.admin.functions import projects_function, profile_function, tasks_function
from TelegramAPI.config.config import permissions_level, SUPERUSER_CHAT_ID, TOKEN_API
from TelegramAPI.BotSource.keyboards import backup_keyboard, start_bot_keyboard
from TelegramAPI.BotSource.admin.buttons.admin_buttons import admin_keyboard, connect_checker
from TelegramAPI.BotSource.admin.buttons import tasks_buttons

bot = TeleBot(TOKEN_API, parse_mode='html')
perms = permissions_level
roles = [
	"'Администратор'", "'Пользователь'"
]
@bot.message_handler(commands=['start'])
def start_command(message):
	perms[message.chat.id] = 'user'
	bot.send_message(message.chat.id, 'Выберите роль:', reply_markup=start_bot_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def chose_role(call):
	chat_id = call.message.chat.id
	if call.data == 'backup_button':
		choose_role_keyboard = InlineKeyboardMarkup()
		user = types.InlineKeyboardButton('Пользователь', callback_data='user')
		admin = types.InlineKeyboardButton('Админ', callback_data='superuser')
		choose_role_keyboard.add(user, admin)
		bot.send_message(chat_id, 'Выберите роль:', reply_markup=choose_role_keyboard)

	# Админ-панель
	elif call.data == 'superuser':
		if str(chat_id) == str(SUPERUSER_CHAT_ID):
			perms[chat_id] = 'superuser'
			bot.send_message(chat_id, 'Вы вошли как администратор')
			print(f'Пользователь ID{chat_id} вошел в систему как {roles[0]}')
			bot.send_message(chat_id, text='Выберите действие:', reply_markup=admin_keyboard())
		else:
			bot.send_message(chat_id, 'У вас нет прав администратора', reply_markup=backup_keyboard())

	elif call.data == 'admin_tasks':
		tasks_function.is_tasks_open(call.message)
	elif call.data == 'admin_tasks_backup_button':
		bot.send_message(chat_id, text='Выберите действие:', reply_markup=admin_keyboard())
	elif call.data == 'tasks_list':
		bot.send_message(chat_id, 'Список заданий:', reply_markup=tasks_function.tasks_list(call.message))
	elif call.data.startswith('task_'):
		tasks_function.is_tasks_list_open(call)
	# Создание таски
	elif call.data == 'create_task':
		bot.send_message(chat_id, 'Выберите проект', reply_markup=tasks_buttons.choose_project(call.message))
	elif call.data.startswith("project_"):
		bot.send_message(chat_id, 'Выберите направление:', reply_markup=tasks_buttons.choose_direction())
	elif call.data.startswith("dir_"):
		bot.send_message(chat_id, text='Напишите задание:')
		bot.register_next_step_handler(call.message, tasks_function.create_task)
	# Удаление таски
	elif call.data == 'delete_task':
		bot.send_message(chat_id, 'Выберите задание:', reply_markup=tasks_function.select_tasks(call.message))
	elif call.data.startswith("check_task_"):
		tasks_function.view_selected_task(call)
	elif call.data.startswith('delete_check_task_'):
		tasks_function.delete_task(call)
	elif call.data == 'backup_delete_task_button':
		tasks_function.view_selected_tasks(call.message)

	elif call.data == 'admin_projects':
		projects_function.is_projects_open(call.message)
	elif call.data == 'admin_projects_backup_button':
		bot.send_message(chat_id, text='Выберите действие:', reply_markup=admin_keyboard())
	# Создание проекта
	elif call.data == 'create_project':
		bot.send_message(chat_id, 'Введите название проекта:')
		bot.register_next_step_handler(call.message, projects_function.add_new_project)
	# Удаление проекта
	elif call.data == 'delete_project':
		bot.send_message(chat_id, 'Выберите проект:', reply_markup=projects_function.select_project(call.message))
	elif call.data.startswith('delete_project_'):
		projects_function.delete_project(call)

	elif call.data == 'admin_profile':
		profile_function.is_profile_open(call)
	elif call.data == 'ssh_key':
		profile_function.is_ssh_key_chose(call)
	elif call.data == 'admin_profile_backup_button':
		bot.send_message(chat_id, text='Выберите действие:', reply_markup=admin_keyboard())
	elif call.data == 'admin_active_profile_backup_button':
		profile_function.is_profile_open(call)

	elif call.data == 'check_connect':
		connect_checker(call)
	# Юзер-панель
	elif call.data == 'user':
		perms[chat_id] = 'user'
		bot.send_message(chat_id, 'Вы вошли как пользователь')


bot.polling(none_stop=True)