import sqlite3 as sq
import time, os


def create():
    db = sq.connect("site_db")
    cursor = db.cursor()
    print("creating database connection file!")
    time.sleep(1)
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS 
        users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT, 
            email TEXT,
            password BLOB) 
        """)
    # #not null varchar(2000)
    # cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS
    #         houses(
    #             house_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #             primer_nombre TEXT,
    #             segundo_nombre TEXT,
    #             primer_apellido TEXT,
    #             segundo_apellido TEXT,
    #             DPI INTEGER,
    #             correo_electronico TEXT,
    #             telefono NUMERIC,
    #             direccion TEXT,
    #             tipo TEXT,
    #             zona NUMERIC,
    #             n_habitaciones NUMERIC,
    #             precio_dolares FLOAT,
    #             precio_quetzales FLOAT,
    #             metros_cuadrados FLOAT,
    #             comentarios_adicionales TEXT,
    #             photos BLOB NOT NULL,
    #             FOREIGN KEY (user_id) REFERENCES user (user_id))
    #         """)
    # cursor.execute("""
    #             CREATE TABLE IF NOT EXISTS
    #             photo(
    #                 photo_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #                 photos BLOB NOT NULL,
    #                 house_id INTEGER,
    #                 FOREIGN KEY (house_id) REFERENCES houses (house_id))
    #             """)

    db.commit()



# Insert user to db
def insert(username, email, password):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""INSERT INTO users (username, email, password) VALUES(?,?,?)""", (username, email, password))
    db.commit()
    db.close()


# basic data check, registered or not
def check_data(email):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT email FROM users WHERE email=(?)""", (email,))
    data = cursor.fetchall()
    if len(data) == 0:
        return True
    else: return False
def check_username(username):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT username FROM users WHERE username=(?)""", (username,))
    data = cursor.fetchall()
    if len(data) == 0:
        return True
    else: return False

def get_email(username):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT email FROM users WHERE username=(?)""", (username,))
    data = cursor.fetchall()
    return data[0]

# -- Basic data check, using email and password to check if user entered correct login info
def check_login_data(username, password):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT username FROM users WHERE username=(?)""", (username,))
    data = cursor.fetchall()
    print(data)
    if len(data) > 0:
        cursor.execute("""SELECT password FROM users WHERE password=(?)""", (password,))
        data = cursor.fetchall()
        print(data)
        if len(data) > 0:
            return True
