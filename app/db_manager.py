import sqlite3 as sq
import time

def create():
    db = sq.connect("site_db")
    cursor = db.cursor()
    print("creating database connection file!")
    time.sleep(1)
    #creating users table
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS 
        users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT, 
            email TEXT,
            password BLOB) 
        """)
    #creating houses table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            houses(
                house_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                primer_nombre TEXT,
                segundo_nombre TEXT,
                primer_apellido TEXT,
                segundo_apellido TEXT,
                DPI INTEGER,
                correo_electronico TEXT,
                telefono NUMERIC,
                direccion TEXT,
                tipo TEXT,
                zona NUMERIC,
                n_habitaciones NUMERIC,
                n_lavados NUMERIC,
                precio_dolares FLOAT,
                precio_quetzales FLOAT,
                metros_cuadrados FLOAT,
                comentarios_adicionales TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES user (user_id))
            """)
    #create photos table
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS
                photos(
                    photos_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    photos BLOB NOT NULL,
                    house_id INTEGER,
                    FOREIGN KEY (house_id) REFERENCES houses (house_id))
                """)

    db.commit()


# Insert user to db
def insert_user(username, email, password):
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

def get_userid(username):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT user_id FROM users WHERE username=(?)""", (username,))
    data = cursor.fetchall()
    return data[0]

# Basic data check, using email and password to check if user entered correct login info
def check_login_data(username, password):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT username FROM users WHERE username=(?)""", (username,))
    data = cursor.fetchall()
    print(type(data))
    if len(data) > 0:
        cursor.execute("""SELECT password FROM users WHERE password=(?)""", (password,))
        data = cursor.fetchall()
        print(data)
        if len(data) > 0:
            return True


# insert house
def insert_house(user_id, name1, name2, lastname1, lastname2, dpi, email1, phone, address, typehome, zone, roomsnumber, roomsbath, pricedol, pricequet, meters, comments, images):
    # name1, name2, lastname1, lastname2, dpi, email1, phone, address, typehome, zone, roomsnumber, roomsbath, pricedol, pricequet, meters, comments, photos

    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""INSERT INTO houses (
        primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, 
        DPI, correo_electronico, telefono, direccion, tipo, zona, n_habitaciones, n_lavados,
        precio_dolares, precio_quetzales, metros_cuadrados, comentarios_adicionales, user_id
    ) VALUES(?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?)""",
                   (str(name1), str(name2), str(lastname1), str(lastname2), int(dpi), str(email1), int(phone), str(address), str(typehome), int(zone),
                    int(roomsnumber), int(roomsbath), float(pricedol), float(pricequet), int(meters), str(comments), int(user_id[0]),))
    house_id = cursor.lastrowid
    for image in images:
        cursor.execute("""INSERT INTO photos (
                photos,
                house_id
            ) VALUES(?, ?)""",
                       (image.read(), house_id,))
    print(house_id)
    db.commit()
    db.close()

def get_houses(zone, typehome, roomsnumber, roomsbath, page_number):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, DPI, correo_electronico, 
    telefono, direccion, tipo, zona, n_habitaciones, n_lavados, precio_dolares, precio_quetzales, metros_cuadrados, 
    comentarios_adicionales, user_id, house_id
    FROM houses 
    WHERE Zona=(?) AND TIPO=(?) AND n_habitaciones=(?) AND n_lavados=(?)
    LIMIT (?) 
    OFFSET (?)""",
                   (zone, typehome, roomsnumber, roomsbath, 5, (page_number-1)*5,))
    data = cursor.fetchall()
    return data

def get_house_images(house_id, num_image):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT photos
    FROM photos 
    WHERE house_id=(?)
    LIMIT 1 OFFSET (?)""",
                   (int(house_id), int(num_image)-1,))
    data = cursor.fetchall()
    print(f'data {data}\nhouse_id {int(house_id)}\nnum_image {int(num_image)-1}\n')
    return data[0]

# create()
# db = sq.connect("site_db")
# cursor = db.cursor()
# cursor.execute("""INSERT INTO houses (
#     primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
#     DPI, correo_electronico, telefono, direccion, tipo, zona, n_habitaciones, n_lavados,
#     precio_dolares, precio_quetzales, metros_cuadrados, comentarios_adicionales, user_id
# ) VALUES(?, ?, ?, ?,
#     ?, ?, ?, ?, ?, ?, ?,
#     ?, ?, ?, ?, ?, ?)""",
#                ("name1", "name2", "lastname1", "lastname2", 123, "email1", 123, "address", "typehome", 123,
#                 123, 123, 123.0, 123.0, 123, "str(comments)", 1,))
# db.commit()
# db.close()