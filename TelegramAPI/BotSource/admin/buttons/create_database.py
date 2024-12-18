import sqlite3

conn = sqlite3.connect('../../../DataBases/users.db')
cursor = conn.cursor()
'''
upload = ("CREATE TABLE users (id int, role text not null, name text not null ,"
          " surname text not null , direction text not null , project text, task text, "
          "active_task text)")
'''

id1 = 876067511
cursor.execute('DELETE FROM users WHERE id = ?', (0,))

