from telebot import types
from telebot.types import InlineKeyboardMarkup

# Таски, проекты, профиль. Основная страница
def admin_keyboard():
	admin_panel = InlineKeyboardMarkup()
	tasks_button = types.InlineKeyboardButton(text='Задания', callback_data='admin_tasks')
	project_button = types.InlineKeyboardButton(text='Проекты', callback_data='admin_projects')
	profile_button = types.InlineKeyboardButton(text='Профиль', callback_data='admin_profile')
	admin_panel.add(tasks_button, project_button, profile_button)
	return admin_panel

def tasks_keyboard():
	tasks_panel = InlineKeyboardMarkup()
	create_task = types.InlineKeyboardButton(text='Добавить задание', callback_data='create_task')
	delete_task = types.InlineKeyboardButton(text='Удалить задание', callback_data='delete_task')
	backup_key = types.InlineKeyboardButton(text='Назад', callback_data='admin_tasks_backup_button')
	tasks_panel.add(create_task, delete_task, backup_key)
	return tasks_panel

def projects_keyboard():
	projects_panel = InlineKeyboardMarkup()
	create_project = types.InlineKeyboardButton(text='Добавить проект', callback_data='create_project')
	delete_project = types.InlineKeyboardButton(text='Удалить проект', callback_data='delete_project')
	backup_key = types.InlineKeyboardButton(text='Назад', callback_data='admin_projects_backup_button')
	projects_panel.add(create_project, delete_project, backup_key)
	return projects_panel

def profile_keyboard():
	profile_panel = InlineKeyboardMarkup()
	ssh_key = types.InlineKeyboardButton(text='SSH-Key', callback_data='ssh_key')
	backup_key = types.InlineKeyboardButton(text='Назад', callback_data='admin_profile_backup_button')
	profile_panel.add(ssh_key, backup_key)
	return profile_panel

def active_profile_keyboard():
	profile_panel = InlineKeyboardMarkup()
	backup_key = types.InlineKeyboardButton(text='Назад', callback_data='admin_active_profile_backup_button')
	profile_panel.add(backup_key)
	return profile_panel