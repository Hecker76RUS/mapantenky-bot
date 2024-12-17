import sqlite3

conn = sqlite3.connect('../../../DataBases/users.db')
cursor = conn.cursor()
'''
upload = ("CREATE TABLE users (id int, role text not null, name text not null ,"
          " surname text not null , direction text not null , project text, task text, "
          "active_task text)")
'''

id1 = 876067511
cursor.execute('DELETE FROM users WHERE id = ?', (id1,))
#conn.commit()
#cursor.execute('INSERT INTO users (id,role,name,surname,direction) VALUES (?,?,?,?,?)', (0,'0','0','0','0',))
conn.commit()
