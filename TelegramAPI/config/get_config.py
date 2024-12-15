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