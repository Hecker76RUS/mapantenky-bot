from TelegramAPI.BotSource.admin.buttons.admin_buttons import profile_keyboard, active_profile_keyboard
from TelegramAPI.config.config import TOKEN_API, ssh_key
from telebot import TeleBot
from TelegramAPI.config import config

bot = TeleBot(TOKEN_API)

def is_profile_open(call):
	chat_id = call.message.chat.id
	photo_path = config.PROFILE
	with open(photo_path, "rb") as photo:
		bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=profile_keyboard())
	return profile_keyboard()

def is_ssh_key_chose(call):
	bot.send_message(call.message.chat.id, text=ssh_key, reply_markup=active_profile_keyboard())
