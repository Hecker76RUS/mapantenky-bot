from telebot import TeleBot
from TelegramAPI.BotSource.buttons.admin.buttons import admin_buttons
from TelegramAPI.config.config import TOKEN_API

bot = TeleBot(TOKEN_API)

def is_tasks_open(call):
	chat_id = call.message.chat.id
	bot.send_message(chat_id, text='Выберите действие:', reply_markup=admin_buttons.tasks_keyboard())
	return admin_buttons.tasks_keyboard()
