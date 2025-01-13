from telebot import TeleBot
from TelegramAPI.config.config import TOKEN_API
bot = TeleBot(TOKEN_API, parse_mode='html')

def err01(message):
	chat_id = message.chat.id
