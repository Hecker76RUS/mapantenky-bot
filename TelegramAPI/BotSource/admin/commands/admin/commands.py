from telebot import TeleBot
from TelegramAPI.config.config import TOKEN_API, SUPERUSER_CHAT_ID
from TelegramAPI.BotSource.admin.functions import projects_function, profile_function, tasks_function

bot = TeleBot(TOKEN_API)

@bot.message_handler(commands=['admin_profile'])
def admin_profile_command(command):
	chat_id = command.message.chat.id
	if str(chat_id) == str(SUPERUSER_CHAT_ID):
		profile_function.is_profile_open(command)

@bot.message_handler(commands=['admin_projects'])
def admin_projects_command(call):
	chat_id = call.message.chat.id
	if str(chat_id) == str(SUPERUSER_CHAT_ID):
		projects_function.is_projects_open(call)

@bot.message_handler(commands=['admin_tasks'])
def admin_tasks_command(call):
	chat_id = call.message.chat.id
	if str(chat_id) == str(SUPERUSER_CHAT_ID):
		tasks_function.is_tasks_open(call)
