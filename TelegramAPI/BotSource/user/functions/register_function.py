import json
import sqlite3

from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from TelegramAPI.config import config
from TelegramAPI.BotSource.user.buttons import register_buttons
from TelegramAPI.BotSource.user.functions import user_function

bot = TeleBot(config.TOKEN_API, parse_mode='html')
register_data = {}
perms = config.permissions_level

def start_registration(message):
	get_name(message)
def get_name(message):
	chat_id = message.chat.id
	if str(chat_id) == str(config.SUPERUSER_CHAT_ID):
		perms[chat_id] = 'superuser'
	else:
		perms[chat_id] = 'user'
	role = perms[chat_id]
	register_data[chat_id] = register_data.get(chat_id, { })
	register_data[chat_id]['role'] = role
	bot.send_message(chat_id, 'Введите свое <b>имя</b>\n(вводить реальное, для корректного отображения информации в профиле)')

def save_temp_name(message):
	chat_id = message.chat.id
	name = message.text
	register_data[chat_id] = register_data.get(chat_id,{})
	register_data[chat_id]['name'] = name
	bot.send_message(chat_id, f'Вас зовут "{name}", верно?',reply_markup=register_buttons.get_name_keyboard())
	return name

def remove_temp_name(message):
	register_data.pop('name', None)
	get_name(message)


def get_surname(message):
	chat_id = message.chat.id
	bot.send_message(chat_id, 'Введите свою <b>фамилию</b>\n(вводить реальную, для корректного отображения информации в профиле)')


def save_temp_surname(message):
	chat_id = message.chat.id
	surname = message.text
	register_data[chat_id] = register_data.get(chat_id, { })
	register_data[chat_id]['surname'] = surname
	bot.send_message(chat_id, f'Ваша фамилия <b>"{surname}"</b>, верно?', reply_markup=register_buttons.get_surname_keyboard())
	return surname


def remove_temp_surname(message):
	register_data.pop('surname', None)
	get_surname(message)

def get_direction(message):
	chat_id = message.chat.id
	name = register_data[chat_id]['name']
	surname = register_data[chat_id]['surname']
	bot.send_message(chat_id, f'Отлично, {name} {surname}.\n\n <b>Теперь выберите направление:</b>', reply_markup=register_buttons.get_direction_keyboard())

def save_direction(call):
	callback_data = call.data
	chat_id = call.message.chat.id
	register_data[chat_id] = register_data.get(chat_id,{})
	register_data[chat_id]['direction'] = callback_data
	bot.send_message(chat_id, 'Отлично! Нажмите кнопку "Завершить" для завершения регистрации', reply_markup=register_buttons.finish_registration())

def finish_registration(message):
	chat_id = message.chat.id
	try:
		conn = sqlite3.connect(config.USERS_PATH)
		cursor = conn.cursor()

		id = chat_id
		role = register_data[chat_id]['role']
		name = register_data[chat_id]['name']
		surname = register_data[chat_id]['surname']
		direction = register_data[chat_id]['direction']

		cursor.execute(
			'INSERT INTO users (id, role, name, surname, direction) VALUES (?,?,?,?,?)',
		               (id, role, name, surname, direction))
		conn.commit()
		if cursor.lastrowid:
			bot.send_message(chat_id, 'Поздравляю! Регистрация завершена🥳')
			user_function.user_panel(message)
		else:
			bot.send_message(chat_id, '<b>ОШИБКА</b> \nПопробуйте позднее')
			start_registration(message)

	except Exception as e:
		print(e)
	finally:
		conn.close()


