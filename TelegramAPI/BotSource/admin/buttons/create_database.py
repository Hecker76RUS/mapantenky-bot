import sqlite3
from TelegramAPI.config import config
conn = sqlite3.connect(config.USERS_PATH)
cursor = conn.cursor()

# upload = 'UPDATE users SET task = ? WHERE id = ?', (task, id1)

# cursor.execute(upload)

cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY,role TEXT NOT NULL,name TEXT NOT NULL,surname TEXT NOT NULL,direction TEXT NOT NULL,change_direction text,project TEXT,task TEXT,active_task TEXT)')
#cursor.execute('DROP TABLE IF EXISTS users')

