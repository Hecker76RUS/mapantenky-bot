from telebot import TeleBot
from config import TOKEN_API
from login import start_command

bot = TeleBot(TOKEN_API)

@bot.message_handler(commands=['start'])
def run_bot(message):
	start_command(message)

bot.polling()
