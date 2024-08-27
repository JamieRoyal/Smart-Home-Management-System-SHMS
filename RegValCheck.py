import re

import bcrypt

import sqlite3

conn = sqlite3.connect('user.db')

conn.execute("CREATE TABLE IF NOT EXISTS user_info(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")

temp_user = ""
temp_pass = ""


def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True


def val_check(user, password):
    global temp_user
    global temp_pass
    temp_user = user
    temp_pass = password

    # Check if Password meets requirements
    if validate_password(temp_pass):
        # If Password meets requirements Encrypt Password
        encrypt_pass = bcrypt.hashpw(temp_pass.encode('utf-8'), bcrypt.gensalt())
        # Once encrypted, store password and username together
        try:
            conn.execute("INSERT INTO user_info (username, password) VALUES (?,?)", (temp_user, encrypt_pass))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("REGISTRATION FAILED: USERNAME ALREADY IN USE")
            return False
    else:
        return False
