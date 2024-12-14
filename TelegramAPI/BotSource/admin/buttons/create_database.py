import sqlite3

conn = sqlite3.connect('../../../DataBases/projects.db')
cursor = conn.cursor()

upload = "CREATE TABLE projects (project_name TEXT, project_name_callback TEXT)"
cursor.execute(upload)
