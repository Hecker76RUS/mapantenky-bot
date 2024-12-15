import sqlite3

conn = sqlite3.connect('../../../DataBases/admin_tasks.db')
cursor = conn.cursor()

upload = "CREATE TABLE tasks (task_id text, check_task text, delete_task text, project text, direction text, task_message text)"
cursor.execute(upload)
