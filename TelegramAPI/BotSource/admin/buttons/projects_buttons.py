import sqlite3
from telebot import TeleBot
from TelegramAPI.config.config import TOKEN_API

bot = TeleBot(TOKEN_API)

def create_project(message):
	chat_id = message.chat.id
	bot.send_message(chat_id, 'Введите название проекта')