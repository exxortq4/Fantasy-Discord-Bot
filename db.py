import sqlite3

db = sqlite3.connect("data.db") # или :memory:
cursor = db.cursor()
db.execute("""CREATE TABLE IF NOT EXISTS users (
    id INT,
    warns INT,
    mutes INT )""")

db.execute("""CREATE TABLE IF NOT EXISTS fun (
    user1 INT,
    user2 INT,
    user3 INT )""")



