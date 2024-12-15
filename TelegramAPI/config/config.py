from TelegramAPI.config.get_config import get_api_key, get_superuser_id, get_ssh_key, get_projects_link, get_admin_task_link
TOKEN_API = get_api_key()
SUPERUSER_CHAT_ID = get_superuser_id()
permissions_level = { }
ssh_key = get_ssh_key()
ADMIN_TASKS_PATH = get_admin_task_link()
PROJECTS_PATH = get_projects_link()
