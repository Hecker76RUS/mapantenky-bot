from telebot.types import InlineKeyboardMarkup
from telebot import TeleBot
from telebot import types

from TelegramAPI.BotSource.admin.functions import projects_function, profile_function
from TelegramAPI.BotSource.admin.buttons import tasks_function
from TelegramAPI.config.config import permissions_level, SUPERUSER_CHAT_ID, TOKEN_API
from TelegramAPI.BotSource.keyboards import backup_keyboard, start_bot_keyboard
from TelegramAPI.BotSource.admin.buttons.admin_buttons import admin_keyboard

bot = TeleBot(TOKEN_API)
perms = permissions_level

@bot.message_handler(commands=['start'])
def start_command(message):
	perms[message.chat.id] = 'user'
	bot.send_message(message.chat.id, 'Выберите роль:', reply_markup=start_bot_keyboard())

## @bot.message_handler(commands=['admin_profile'])
## def admin_profile_command(command):
##	admin_profile_command(command)

@bot.callback_query_handler(func=lambda call: call.data in ['user', 'superuser', 'backup_button']
                                              or call.data in ['admin_tasks', 'admin_projects', 'admin_profile']
                                              or call.data in ['create_task', 'delete_task']
                                              or call.data in ['create_project', 'delete_project']
                                              or call.data in ['ssh_key', 'admin_profile_backup_button', 'admin_active_profile_backup_button'])

def chose_role(call):
	chat_id = call.message.chat.id
	if call.data == 'backup_button':
		choose_role_keyboard = InlineKeyboardMarkup()
		user = types.InlineKeyboardButton('Пользователь', callback_data='user')
		admin = types.InlineKeyboardButton('Админ', callback_data='superuser')
		choose_role_keyboard.add(user, admin)
		bot.send_message(chat_id, 'Выберите роль:', reply_markup=choose_role_keyboard)
	elif call.data == 'superuser':
		if str(chat_id) == str(SUPERUSER_CHAT_ID):
			perms[chat_id] = 'superuser'
			bot.send_message(chat_id, 'Вы вошли как администратор')
			bot.send_message(chat_id, text='Выберите действие:', reply_markup=admin_keyboard())
		else:
			bot.send_message(chat_id, 'У вас нет прав администратора', reply_markup=backup_keyboard())
	elif call.data == 'admin_tasks':
		tasks_function.is_tasks_open(call)

	elif call.data == 'admin_projects':
		projects_function.is_projects_open(call)
	elif call.data == 'create_project':
		projects_function.add_new_project(call)

	elif call.data == 'admin_profile':
		profile_function.is_profile_open(call)
	elif call.data == 'ssh_key':
		profile_function.is_ssh_key_chose(call)
	elif call.data == 'admin_profile_backup_button':
		bot.send_message(chat_id, text='Выберите действие:', reply_markup=admin_keyboard())
	elif call.data == 'admin_active_profile_backup_button':
		profile_function.is_profile_open(call)

	elif call.data == 'user':
		perms[chat_id] = 'user'
		bot.send_message(chat_id, 'Вы вошли как пользователь')



bot.polling(none_stop=True)