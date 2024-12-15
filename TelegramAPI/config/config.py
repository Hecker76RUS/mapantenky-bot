from TelegramAPI.config.get_token import get_token, get_superuser_id
from TelegramAPI.config.get_ssh import get_ssh_key
from TelegramAPI.config.get_db_path import get_admin_tasks, get_projects


TOKEN_API = get_token()
SUPERUSER_CHAT_ID = get_superuser_id()

PROJECTS = [( 'Робот-дворецкий', 'robotButler'), ('Умный свет', 'smartLight')]

permissions_level = { }

ssh_key = get_ssh_key()

ADMIN_TASKS_PATH = get_admin_tasks()
PROJECTS_PATH = get_projects()