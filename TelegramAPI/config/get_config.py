import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def get_api_key():
    return load_config().get("api_key")

def get_superuser_id():

    return load_config().get("superuser_id")

def get_ssh_key():
    return load_config().get("ssh_key")

def get_admin_task_link():
    return load_config().get("admin_task_link")

def get_projects_link():
    return load_config().get("projects_link")

def get_users_link():
    return load_config().get("users_link")

def get_choose_action():
    return load_config().get("choose_action")

def get_create_project():
    return load_config().get("create_project")

def get_create_task():
    return load_config().get("create_task")

def get_delete_project():
    return load_config().get("delete_project")

def get_delete_task():
    return load_config().get("delete_task")

def get_profile():
    return load_config().get("profile")

def get_projects():
    return load_config().get("projects")

def get_tasks():
    return load_config().get("tasks")