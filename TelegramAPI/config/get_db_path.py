def get_admin_tasks():
	admin_tasks = open('C:\\Users\\kudrii\\PycharmProjects\\Mapantenky_bot\\TelegramAPI\\config\\admin_tasks_db_path.txt', 'r')
	is_admin_tasks = admin_tasks.read()
	admin_tasks.close()
	return is_admin_tasks

def get_projects():
	projects_path = open('C:\\Users\\kudrii\\PycharmProjects\\Mapantenky_bot\\TelegramAPI\\config\\projects_db_path.txt', 'r')
	is_projects_path = projects_path.read()
	projects_path.close()
	return is_projects_path