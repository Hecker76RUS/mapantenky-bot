from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot, types

from TelegramAPI.BotSource.admin.functions import projects_function, profile_function, tasks_function
from TelegramAPI.BotSource.user.functions.register_function import get_name
from TelegramAPI.config.config import permissions_level, SUPERUSER_CHAT_ID, TOKEN_API
from TelegramAPI.config import config
from TelegramAPI.BotSource.keyboards import backup_keyboard, start_bot_keyboard
from TelegramAPI.BotSource.admin.buttons.admin_buttons import admin_keyboard, connect_checker
from TelegramAPI.BotSource.admin.buttons import tasks_buttons, projects_buttons
from TelegramAPI.BotSource.user.functions import register_function, login_function, user_function, user_tasks_function


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
def check_perms(chat_id):
    if str(chat_id) == str(SUPERUSER_CHAT_ID):
        perms[chat_id] = 'superuser'
    else:
        perms[chat_id] = 'user'
    return perms[chat_id]

def admin(message):
    chat_id = message.chat.id
    photo_path = config.CHOOSE_ACTION
    with open(photo_path, "rb") as photo:
        bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=admin_keyboard())

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
        photo_path = config.CHOOSE_ACTION
        bot.send_message(chat_id, 'Вы вошли как администратор')
        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=admin_keyboard())
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
    help_text += "/admin - (админ) Открыть админ-панель\n"
    help_text += "/tasks - (админ) Управление задачами\n"
    help_text += "/projects - (админ) Управление проектами\n"
    help_text += "/profile - (админ) Открыть профиль\n"
    help_text += "/create_task - (админ) Создать задачу\n"
    help_text += "/delete_task - (админ) Удалить задачу\n"
    help_text += "/create_project - (админ) Создать проект\n"
    help_text += "/delete_project - (админ) Удалить проект\n"
    help_text += "/help - Список команд\n"
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['admin'])
def admin_panel_command(message):
    chat_id = message.chat.id
    if str(chat_id) == str(SUPERUSER_CHAT_ID):
        perms[chat_id] = 'superuser'
        photo_path = config.CHOOSE_ACTION
        bot.send_message(chat_id, 'Вы вошли как администратор')
        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=admin_keyboard())
    else:
        bot.send_message(chat_id, 'У вас нет прав администратора', reply_markup=backup_keyboard())

@bot.message_handler(commands=['tasks'])
def tasks_command(message):
    if check_perms(message.chat.id) == 'superuser':
        bot.send_message(message.chat.id, "Управление задачами", reply_markup=tasks_function.tasks_list(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['create_task'])
def create_task_command(message):
    if check_perms(message.chat.id) == 'superuser':
        tasks_function.choose_project(message)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['delete_task'])
def delete_task_command(message):
    if check_perms(message.chat.id) == 'superuser':
        tasks_function.select_tasks(message)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['projects'])
def projects_command(message):
    if check_perms(message.chat.id) == 'superuser':
        bot.send_message(message.chat.id, "Управление проектами", reply_markup=projects_function.is_projects_open(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['create_project'])
def create_project_command(message):
    if check_perms(message.chat.id) == 'superuser':
        projects_function.add_new_project(message)
        bot.register_next_step_handler(message, projects_buttons.add_new_project_keyboard)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['delete_project'])
def delete_project_command(message):
    if check_perms(message.chat.id) == 'superuser':
        bot.send_message(message.chat.id, "Выберите проект:", reply_markup=projects_function.select_project(message))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

# ========= КНОПКИ =============
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    callbacks = {

        # ======= Админ панель =========
        # Админ панель
        'backup_button': lambda: send_role_selection(chat_id),
        'superuser': lambda: check_superuser(chat_id),
        'admin_tasks': lambda: tasks_function.is_tasks_open(call.message),
        'admin_profile': lambda: profile_function.is_profile_open(call),

        # Панель "Задания"
        'admin_tasks_backup_button': lambda: admin(call.message),
        'tasks_list': lambda: bot.send_message(chat_id, 'Список заданий:', reply_markup=tasks_function.tasks_list(call.message)),
        'create_task': lambda: tasks_function.choose_project(call.message),
        'delete_task': lambda: tasks_function.select_tasks(call.message),
        'backup_task_select_button': lambda: tasks_function.is_tasks_open(call.message),
        'backup_task_list_button': lambda: tasks_function.is_tasks_open(call.message),
        'backup_task_choose_project_button': lambda: tasks_function.is_tasks_open(call.message),
        'backup_tasks_choose_direction_button': lambda: tasks_function.choose_project(call.message),
        'backup_delete_tasks_button': lambda:tasks_function.select_tasks(call.message),

        # Панель "Проекты"
        'admin_projects': lambda: projects_function.is_projects_open(call.message),
        'admin_projects_backup_button': lambda: admin(call.message),
        'delete_project': lambda: projects_function.select_project(call.message),
        'projects_list': lambda: bot.send_message(chat_id, 'Существующие проекты:', reply_markup=projects_buttons.projects_list(call.message)),
        'backup_projects_list_button': lambda: projects_function.is_projects_open(call.message),
        'backup_projects_select_button': lambda: projects_function.is_projects_open(call.message),

        # Панель "Профиль"
        'ssh_key': lambda: profile_function.is_ssh_key_chose(call),
        'admin_profile_backup_button': lambda: admin(call.message),
        'admin_active_profile_backup_button': lambda: profile_function.is_profile_open(call),

        # ======== Юзер панель ==========

        # Регистрация
        'surname_true': lambda: register_function.get_direction(call.message),
        'finish_registration': lambda: register_function.finish_registration(call.message),
        'backup_user_task_list': lambda: user_function.user_panel(call.message),
        'backup_user_show_tasks': lambda: user_tasks_function.user_tasks_panel(call.message),

        # Юзер панель
        "user_tasks": lambda: user_tasks_function.choose_user_project(call.message),
    }

    # Проверка словаря
    if call.data in callbacks:
        callbacks[call.data]()

    # call.data.startswith
    elif call.data.startswith('task_'):
        tasks_function.is_tasks_list_open(call)
    elif call.data.startswith("project_"):
        tasks_function.save_project_data(call)
    elif call.data.startswith("dir_"):
        tasks_function.save_direction_data(call)
        bot.register_next_step_handler(call.message, tasks_function.create_task)
    elif call.data.startswith('delete_project_'):
        projects_function.delete_project(call)
    elif call.data.startswith("check_task_"):
        tasks_function.view_selected_task(call)
    elif call.data.startswith('delete_check_task_'):
        tasks_function.delete_task(call)
    elif call.data.startswith('users_project_'):
        user_tasks_function.user_tasks_panel(call)
    elif call.data.startswith('u_task_'):
        user_tasks_function.show_user_task(call)
    elif call.data.startswith('claim_u_task_'):
        user_tasks_function.claim_task(call)

    # ========== ИСКЛЮЧЕНИЯ ===========
    elif call.data == 'create_project':
        projects_function.add_new_project(call.message)
        bot.register_next_step_handler(call.message, projects_buttons.add_new_project_keyboard)
    elif call.data == 'check_connect':
        connect_checker(call)
        admin(call.message)

    # ========== РЕГИСТРАЦИЯ ===========
    elif call.data == 'user':
        login_function.check_registration(call.message)
        bot.register_next_step_handler(call.message, register_function.save_temp_name)

    elif call.data == 'name_true':
        register_function.get_surname(call.message)
        bot.register_next_step_handler(call.message, register_function.save_temp_surname)
    elif call.data == 'name_false':
        register_function.remove_temp_name(call.message)
        bot.register_next_step_handler(call.message, register_function.save_temp_name)

    elif call.data == 'surname_false':
        register_function.remove_temp_surname(call.message)
        bot.register_next_step_handler(call.message, register_function.save_temp_surname)
    elif call.data.startswith('user_dir'):
        register_function.save_direction(call)
    else:
        bot.send_message(chat_id, 'Неизвестная команда.')

bot.polling(none_stop=True)
