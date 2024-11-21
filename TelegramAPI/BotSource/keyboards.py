from telebot import types
from telebot.types import InlineKeyboardMarkup
from telebot import TeleBot
from TelegramAPI.BotSource.config import TOKEN_API

bot = TeleBot(TOKEN_API)
@bot.callback_query_handler(func = lambda call: call.data == 'back_to_login')
def backup_keyboard():
	back_keyboard = InlineKeyboardMarkup()
	backup_key = types.InlineKeyboardButton(text='Назад', callback_data='backup_button')
	back_keyboard.add(backup_key)

def keys():
	menu = types.InlineKeyboardMarkup()
	menu_button = types.InlineKeyboardButton(text='1', callback_data='one')
	menu.add(menu_button)
	return menu_button