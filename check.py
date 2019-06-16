import sqlite3
import os
database = sqlite3.connect('db.sqlite3')
c = database.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(c.fetchall())
# c.execute("SELECT * FROM auth_user")
# # print(c.fetchall())
# c.execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'auth_user' AND type = 'table'")
# print(c.fetchall())
# print(os.path.join(os.path.dirname(__file__)))
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# c.execute("delete FROM users_keywords where id_keyword < 101")
# database.commit()
# print(c.fetchall())


c.execute("SELECT * FROM users_keywords_id_profile")
print('users_keywords_id_profile')
print(c.fetchall())
c.execute("SELECT * FROM users_keywords")
print('users_keywords')
print(c.fetchall())
c.execute("SELECT * FROM users_profiles")
print('users_profiles')
print(c.fetchall())

li = {'d':213}
b = {'a':li['d']}
print(b['a'])
