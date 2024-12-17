from TelegramAPI.config.get_config import get_api_key, get_superuser_id, get_ssh_key, get_projects_link, \
	get_admin_task_link, get_choose_action, get_create_project, get_create_task, get_delete_task, get_delete_project, \
	get_profile, get_projects, get_tasks, get_users_link

TOKEN_API = get_api_key()
SUPERUSER_CHAT_ID = get_superuser_id()
permissions_level = { }
ssh_key = get_ssh_key()
ADMIN_TASKS_PATH = get_admin_task_link()
PROJECTS_PATH = get_projects_link()
USERS_PATH = get_users_link()
CHOOSE_ACTION = get_choose_action()
CREATE_PROJECT = get_create_project()
CREATE_TASK = get_create_task()
DELETE_TASK = get_delete_task()
DELETE_PROJECT = get_delete_project()
PROFILE = get_profile()
PROJECTS = get_projects()
TASKS =  get_tasks()
