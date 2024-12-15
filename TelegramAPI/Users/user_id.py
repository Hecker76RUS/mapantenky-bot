from TelegramAPI.config.config import TOKEN_API
from telebot import TeleBot
from telebot import types
from TelegramAPI.config.config import permissions_level

bot = TeleBot(TOKEN_API)
perms = permissions_level

@bot.message_handler(commands=['start'])
def run_bot(message):
	perms[message.chat.id] = 'user'
	choose_role_keyboard =types.InlineKeyboardMarkup()
	choose_role_keyboard.add(types.InlineKeyboardButton('Пользователь', callback_data='user'))
	choose_role_keyboard.add(types.InlineKeyboardButton('Админ', callback_data='superuser'))
	bot.send_message(message.chat.id, 'Выберите роль:', reply_markup=choose_role_keyboard)


from telebot.types import InlineKeyboardMarkup
from telebot import TeleBot, types
from TelegramAPI.BotSource.admin.functions import projects_function, profile_function, tasks_function
from TelegramAPI.BotSource.handlers import admin_panel
from TelegramAPI.config.config import permissions_level, SUPERUSER_CHAT_ID, TOKEN_API
from TelegramAPI.BotSource.keyboards import backup_keyboard, start_bot_keyboard
from TelegramAPI.BotSource.admin.buttons.admin_buttons import admin_keyboard, connect_checker
from TelegramAPI.BotSource.admin.buttons import tasks_buttons

bot = TeleBot(TOKEN_API, parse_mode='html')
perms = permissions_level
roles = ["'Администратор'", "'Пользователь'"]

# =================== Обработчики команд ===================
@bot.message_handler(commands=['start'])
def start_command(message):
    perms[message.chat.id] = 'user'
    bot.send_message(message.chat.id, 'Выберите роль:', reply_markup=start_bot_keyboard())

@bot.message_handler(commands=['admin'])
def admin_panel_command(message):
    chat_id = message.chat.id
    if str(chat_id) == str(SUPERUSER_CHAT_ID):
        perms[chat_id] = 'superuser'
        bot.send_message(chat_id, 'Вы вошли как администратор')
        print(f'Пользователь ID{chat_id} вошел в систему как {roles[0]}')
        bot.send_message(chat_id, text='Выберите действие:', reply_markup=admin_keyboard())
    else:
        bot.send_message(chat_id, 'У вас нет прав администратора', reply_markup=backup_keyboard())

@bot.message_handler(commands=['tasks'])
def tasks_command(message):
    tasks_function.is_tasks_open(message)

@bot.message_handler(commands=['projects'])
def projects_command(message):
    projects_function.is_projects_open(message)

@bot.message_handler(commands=['profile'])
def profile_command(message):
    profile_function.is_profile_open(types.CallbackQuery(message=message))

@bot.message_handler(commands=['create_task'])
def create_task_command(message):
    bot.send_message(message.chat.id, 'Выберите проект', reply_markup=tasks_buttons.choose_project(message))

@bot.message_handler(commands=['delete_task'])
def delete_task_command(message):
    bot.send_message(message.chat.id, 'Выберите задание:', reply_markup=tasks_function.select_tasks(message))

@bot.message_handler(commands=['create_project'])
def create_project_command(message):
    bot.send_message(message.chat.id, 'Введите название проекта:')
    bot.register_next_step_handler(message, projects_function.add_new_project)

@bot.message_handler(commands=['delete_project'])
def delete_project_command(message):
    bot.send_message(message.chat.id, 'Выберите проект:', reply_markup=projects_function.select_project(message))

# =================== Обработчик callback-кнопок ===================
@bot.callback_query_handler(func=lambda call: True)
def chose_role(call):
    chat_id = call.message.chat.id
    if call.data == 'backup_button':
        choose_role_keyboard = InlineKeyboardMarkup()
        user = types.InlineKeyboardButton('Пользователь', callback_data='user')
        admin = types.InlineKeyboardButton('Админ', callback_data='superuser')
        choose_role_keyboard.add(user, admin)
        bot.send_message(chat_id, 'Выберите роль:', reply_markup=choose_role_keyboard)

    elif call.data == 'superuser':
        if str(chat_id) == str(SUPERUSER_CHAT_ID):
            perms[chat_id] = 'superuser'
            bot.send_message(chat_id, 'Вы вошли как администратор')
            bot.send_message(chat_id, text='Выберите действие:', reply_markup=admin_keyboard())
        else:
            bot.send_message(chat_id, 'У вас нет прав администратора', reply_markup=backup_keyboard())

    elif call.data == 'admin_tasks':
        tasks_function.is_tasks_open(call.message)
    elif call.data.startswith('task_'):
        tasks_function.is_tasks_list_open(call)
    elif call.data.startswith("project_"):
        bot.send_message(chat_id, 'Выберите направление:', reply_markup=tasks_buttons.choose_direction())
    elif call.data.startswith("dir_"):
        bot.send_message(chat_id, text='Напишите задание:')
        bot.register_next_step_handler(call.message, tasks_function.create_task)
    elif call.data.startswith('delete_project_'):
        projects_function.delete_project(call)
    elif call.data == 'admin_profile':
        profile_function.is_profile_open(call)

# =================== Запуск бота ===================
bot.polling(none_stop=True)

from telebot import TeleBot, types
from TelegramAPI.config.config import TOKEN_API, SUPERUSER_CHAT_ID

bot = TeleBot(TOKEN_API, parse_mode='html')
perms = {}  # Словарь для хранения ролей пользователей (например: chat_id -> роль)

# Устанавливаем команды (показываются всем, но доступны только админам)
bot.set_my_commands([
    types.BotCommand("start", "Запуск бота"),
    types.BotCommand("admin", "Открыть админ-панель"),
    types.BotCommand("tasks", "Управление задачами"),
    types.BotCommand("projects", "Управление проектами"),
    types.BotCommand("profile", "Открыть профиль"),
    types.BotCommand("create_task", "Создать задачу"),
    types.BotCommand("delete_task", "Удалить задачу"),
    types.BotCommand("create_project", "Создать проект"),
    types.BotCommand("delete_project", "Удалить проект"),
    types.BotCommand("help", "Список команд"),
])

# Проверка на администратора
def is_admin(chat_id):
    return str(chat_id) == str(SUPERUSER_CHAT_ID) or perms.get(chat_id) == 'superuser'

# =================== Обработчики команд ===================

@bot.message_handler(commands=['start'])
def start_command(message):
    perms[message.chat.id] = 'user'  # По умолчанию пользователь
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите роль:", reply_markup=start_bot_keyboard())

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Список команд доступен только администраторам.")

@bot.message_handler(commands=['admin'])
def admin_panel_command(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Вы вошли в админ-панель", reply_markup=admin_keyboard())
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['tasks'])
def tasks_command(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Управление задачами", reply_markup=tasks_function.tasks_list(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['create_task'])
def create_task_command(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Выберите проект", reply_markup=tasks_buttons.choose_project(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['delete_task'])
def delete_task_command(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Выберите задание:", reply_markup=tasks_function.select_tasks(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['projects'])
def projects_command(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Управление проектами", reply_markup=projects_function.is_projects_open(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['create_project'])
def create_project_command(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Введите название проекта:")
        bot.register_next_step_handler(message, projects_function.add_new_project)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['delete_project'])
def delete_project_command(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Выберите проект:", reply_markup=projects_function.select_project(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

# =================== Запуск бота ===================
bot.polling(none_stop=True)
