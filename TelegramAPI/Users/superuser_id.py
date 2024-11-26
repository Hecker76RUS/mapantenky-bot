import sqlite3


def create_database():
	# Connect to SQLite database. Database will be created if it doesn't exist
	conn = sqlite3.connect('../BotSource/projects.db')

	# Create a cursor object
	cursor = conn.cursor()

	# Create table
	cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    project_name TEXT NOT NULL);
    ''')

	# Commit the transaction
	conn.commit()

	# Close the connection
	conn.close()


create_database()
