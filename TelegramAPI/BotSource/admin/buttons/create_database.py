import sqlite3

conn = sqlite3.connect('../../../DataBases/admin_tasks.db')
cursor = conn.cursor()

upload = "DELETE FROM tasks WHERE task_message = 'DW'"
cursor.execute(upload)
conn.commit()
conn.close()