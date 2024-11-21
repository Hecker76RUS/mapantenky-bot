from telebot.types import InlineKeyboardMarkup
from telebot import TeleBot
from telebot import types
from TelegramAPI.BotSource.config import permissions_level, SUPERUSER_CHAT_ID
from config import TOKEN_API

bot = TeleBot(TOKEN_API)
perms = permissions_level

@bot.message_handler(commands=['start'])
def start_command(message):
	perms[message.chat.id] = 'user'
	choose_role_keyboard = InlineKeyboardMarkup()
	user = types.InlineKeyboardButton('Пользователь', callback_data='user')
	admin = types.InlineKeyboardButton('Админ', callback_data='superuser')
	choose_role_keyboard.add(user, admin)
	bot.send_message(message.chat.id, 'Выберите роль:', reply_markup=choose_role_keyboard)
	return choose_role_keyboard

@bot.callback_query_handler(func=lambda call: call.data in ['user', 'superuser'] or call.data in ['back_to_login'])
def chose_role(call):
	if call.data == 'superuser':
		chat_id = call.message.chat.id
		if str(chat_id) == str(SUPERUSER_CHAT_ID):
			perms[chat_id] = 'superuser'
			bot.send_message(chat_id, 'Вы вошли как администратор')
			bot.send_message(chat_id, 'Выберите действие:')
		else:
			back_keyboard = InlineKeyboardMarkup()
			backup_key = types.InlineKeyboardButton(text='Назад', callback_data='backup_button')
			back_keyboard.add(backup_key)
			bot.send_message(chat_id, 'У вас нет прав администратора', reply_markup=back_keyboard)
			if call.data == 'backup_button':
				choose_role_keyboard = InlineKeyboardMarkup()
				user = types.InlineKeyboardButton('Пользователь', callback_data='user')
				admin = types.InlineKeyboardButton('Админ', callback_data='superuser')
				choose_role_keyboard.add(user, admin)
				bot.send_message(chat_id, 'Выберите роль:', reply_markup=choose_role_keyboard)
bot.polling()