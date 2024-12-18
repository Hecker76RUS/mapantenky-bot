import sqlite3

conn = sqlite3.connect('../../../DataBases/admin_tasks.db')
cursor = conn.cursor()
'''
upload = ("CREATE TABLE users (id int, role text not null, name text not null ,"
          " surname text not null , direction text not null , project text, task text, "
          "active_task text)")
'''

id1 = 876067511
#cursor.execute('DELETE FROM users WHERE role = ?', ('0',))
cursor.execute('ALTER TABLE tasks ADD COLUMN claim_project text')

