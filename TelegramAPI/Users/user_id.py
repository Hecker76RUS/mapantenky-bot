from TelegramAPI.BotSource.config import TOKEN_API, SUPERUSER_CHAT_ID
from telebot import TeleBot
from telebot import types
from TelegramAPI.BotSource.config import permissions_level

bot = TeleBot(TOKEN_API)
perms = permissions_level

@bot.message_handler(commands=['start'])
def run_bot(message):
	perms[message.chat.id] = 'user'
	choose_role_keyboard =types.InlineKeyboardMarkup()
	choose_role_keyboard.add(types.InlineKeyboardButton('Пользователь', callback_data='user'))
	choose_role_keyboard.add(types.InlineKeyboardButton('Админ', callback_data='superuser'))
	bot.send_message(message.chat.id, 'Выберите роль:', reply_markup=choose_role_keyboard)

