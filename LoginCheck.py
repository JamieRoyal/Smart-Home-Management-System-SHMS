import bcrypt

import sqlite3

conn = sqlite3.connect('user.db')
conn.execute("CREATE TABLE IF NOT EXISTS user_info(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
cursor = conn.cursor()


def login_check(user, passw):
    query = "SELECT password FROM user_info WHERE username=?"
    cursor.execute(query, (user,))
    row = cursor.fetchone()

    if row:
        password = row[0]
        print(f"Password for user {user}: {password}")
        if bcrypt.checkpw(passw.encode('utf-8'), password):
            return True
        else:
            return False
    else:
        print("No User found")
        return False
