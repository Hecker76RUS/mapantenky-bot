from TelegramAPI.BotSource.buttons.admin.buttons.admin_buttons import profile_keyboard, active_profile_keyboard
from TelegramAPI.config.config import TOKEN_API, ssh_key
from telebot import TeleBot

bot = TeleBot(TOKEN_API)

def is_profile_open(call):
	chat_id = call.message.chat.id
	bot.send_message(chat_id, text='Выберите действие:', reply_markup=profile_keyboard())
	return profile_keyboard()

def is_ssh_key_chose(call):
	bot.send_message(call.message.chat.id, text=ssh_key, reply_markup=active_profile_keyboard())
