from telebot import TeleBot
from TelegramAPI.config.config import TOKEN_API
from TelegramAPI.BotSource.login import start_command

bot = TeleBot(TOKEN_API)

@bot.message_handler(commands=['start'])
def run_bot(message):
	start_command(message)

bot.polling()
