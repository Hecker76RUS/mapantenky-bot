from telebot import TeleBot
from TelegramAPI.config import config
from TelegramAPI.BotSource.user.buttons import user_buttons
bot = TeleBot(config.TOKEN_API, parse_mode='html')

def user_panel(message):
	chat_id = message.chat.id
	bot.send_message(chat_id, 'Выберите действие', reply_markup=user_buttons.user_keyboard())