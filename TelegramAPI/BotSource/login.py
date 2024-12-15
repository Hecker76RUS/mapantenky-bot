from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot, types

from TelegramAPI.BotSource.admin.functions import projects_function, profile_function, tasks_function
from TelegramAPI.config.config import permissions_level, SUPERUSER_CHAT_ID, TOKEN_API
from TelegramAPI.BotSource.keyboards import backup_keyboard, start_bot_keyboard
from TelegramAPI.BotSource.admin.buttons.admin_buttons import admin_keyboard, connect_checker
from TelegramAPI.BotSource.admin.buttons import tasks_buttons

bot = TeleBot(TOKEN_API, parse_mode='html')
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
perms = permissions_level
roles = ["'Администратор'", "'Пользователь'"]

# =================== Общие функции ===================
def send_role_selection(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Пользователь', callback_data='user'),
        InlineKeyboardButton('Админ', callback_data='superuser')
    )
    bot.send_message(chat_id, 'Выберите роль:', reply_markup=keyboard)

def check_superuser(chat_id):
    if str(chat_id) == str(SUPERUSER_CHAT_ID):
        perms[chat_id] = 'superuser'
        bot.send_message(chat_id, 'Вы вошли как администратор')
        print(f'Пользователь ID{chat_id} вошел в систему как {roles[0]}')
        bot.send_message(chat_id, 'Выберите действие:', reply_markup=admin_keyboard())
    else:
        bot.send_message(chat_id, 'У вас нет прав администратора', reply_markup=backup_keyboard())

# =================== Обработчики ===================
@bot.message_handler(commands=['start'])
def start_command(message):
    perms[message.chat.id] = 'user'
    bot.send_message(message.chat.id, 'Выберите роль:', reply_markup=start_bot_keyboard())

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = "Список доступных команд:\n"
    help_text += "/start - Запуск бота\n"
    help_text += "/admin - Открыть админ-панель\n"
    help_text += "/tasks - Управление задачами\n"
    help_text += "/projects - Управление проектами\n"
    help_text += "/profile - Открыть профиль\n"
    help_text += "/create_task - Создать задачу\n"
    help_text += "/delete_task - Удалить задачу\n"
    help_text += "/create_project - Создать проект\n"
    help_text += "/delete_project - Удалить проект\n"
    help_text += "/help - Список команд\n"
    bot.send_message(message.chat.id, help_text)

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
    if check_superuser(message.chat.id) == 'superuser':
        bot.send_message(message.chat.id, "Управление задачами", reply_markup=tasks_function.tasks_list(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['create_task'])
def create_task_command(message):
    if check_superuser(message.chat.id) == 'superuser':
        bot.send_message(message.chat.id, "Выберите проект", reply_markup=tasks_buttons.choose_project(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['delete_task'])
def delete_task_command(message):
    if check_superuser(message.chat.id) == 'superuser':
        bot.send_message(message.chat.id, "Выберите задание:", reply_markup=tasks_function.select_tasks(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['projects'])
def projects_command(message):
    if check_superuser(message.chat.id) == 'superuser':
        bot.send_message(message.chat.id, "Управление проектами", reply_markup=projects_function.is_projects_open(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['create_project'])
def create_project_command(message):
    if check_superuser(message.chat.id) == 'superuser':
        bot.send_message(message.chat.id, "Введите название проекта:")
        bot.register_next_step_handler(message, projects_function.add_new_project)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['delete_project'])
def delete_project_command(message):
    if check_superuser(message.chat.id) == 'superuser':
        bot.send_message(message.chat.id, "Выберите проект:", reply_markup=projects_function.select_project(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    callbacks = {
        # Админ панель
        'backup_button': lambda: send_role_selection(chat_id),
        'superuser': lambda: check_superuser(chat_id),
        'admin_tasks': lambda: tasks_function.is_tasks_open(call.message),
        'check_connect': lambda: connect_checker(call),

        # Панель "Задания"
        'admin_tasks_backup_button': lambda: bot.send_message(chat_id, 'Выберите действие:', reply_markup=admin_keyboard()),
        'tasks_list': lambda: bot.send_message(chat_id, 'Список заданий:', reply_markup=tasks_function.tasks_list(call.message)),
        'create_task': lambda: bot.send_message(chat_id, 'Выберите проект', reply_markup=tasks_buttons.choose_project(call.message)),
        'delete_task': lambda: bot.send_message(chat_id, 'Выберите задание:', reply_markup=tasks_function.select_tasks(call.message)),

        # Панель "Проекты"
        'admin_projects': lambda: projects_function.is_projects_open(call.message),
        'admin_projects_backup_button': lambda: bot.send_message(chat_id, 'Выберите действие:', reply_markup=admin_keyboard()),
        'create_project': lambda: bot.send_message(chat_id, 'Введите название проекта:', bot.register_next_step_handler(call.message, projects_function.add_new_project)),
        'delete_project': lambda: bot.send_message(chat_id, 'Выберите проект:', reply_markup=projects_function.select_project(call.message)),

        # Панель "Профиль"
        'admin_profile': lambda: profile_function.is_profile_open(call),
        'ssh_key': lambda: profile_function.is_ssh_key_chose(call),
        'admin_profile_backup_button': lambda: bot.send_message(chat_id, 'Выберите действие:', reply_markup=admin_keyboard()),
        'user': lambda: bot.send_message(chat_id, 'Вы вошли как пользователь')
    }

    # Проверка словаря
    if call.data in callbacks:
        callbacks[call.data]()

    # call.data.startswith
    elif call.data.startswith('task_'):
        tasks_function.is_tasks_list_open(call)
    elif call.data.startswith("project_"):
        bot.send_message(chat_id, 'Выберите направление:', reply_markup=tasks_buttons.choose_direction())
    elif call.data.startswith("dir_"):
        bot.send_message(chat_id, 'Напишите задание:')
        bot.register_next_step_handler(call.message, tasks_function.create_task)
    elif call.data.startswith('delete_project_'):
        projects_function.delete_project(call)
    elif call.data.startswith("check_task_"):
        tasks_function.view_selected_task(call)
    elif call.data.startswith('delete_check_task_'):
        tasks_function.delete_task(call)
    else:
        bot.send_message(chat_id, 'Неизвестная команда.')

bot.polling(none_stop=True)
