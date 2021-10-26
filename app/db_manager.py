import sqlite3 as sq
import time

import sqlalchemy

from app import db as db


class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(40))


class Houses(db.Model):
    __tablename__ = "houses"
    house_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primer_nombre = db.Column(db.String(200))
    segundo_nombre = db.Column(db.String(200))
    primer_apellido = db.Column(db.String(200))
    segundo_apellido = db.Column(db.String(200))
    DPI = db.Column(db.Integer)
    correo_electronico = db.Column(db.String(200))
    telefono = db.Column(db.Integer)
    direccion = db.Column(db.String(200))
    tipo = db.Column(db.String(200))
    zona = db.Column(db.Integer)
    n_habitaciones = db.Column(db.Integer)
    n_lavados = db.Column(db.Integer)
    precio_dolares = db.Column(db.FLOAT)
    precio_quetzales = db.Column(db.FLOAT)
    metros_cuadrados = db.Column(db.FLOAT)
    comentarios_adicionales = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


class Photos(db.Model):
    __tablename__ = "photos"
    photos_id = db.Column(db.Integer, primary_key=True)
    photos = db.Column(db.LargeBinary)
    house_id = db.Column(db.Integer)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.house_id'))


class Citas(db.Model):
    __tablename__ = "citas"
    cita_id = db.Column(db.Integer, primary_key=True)
    name3 = db.Column(db.String(200))
    name4 = db.Column(db.String(200))
    lastname3 = db.Column(db.String(200))
    lastname4 = db.Column(db.String(200))
    dpi1 = db.Column(db.Integer)
    email2 = db.Column(db.String(200))
    phone1 = db.Column(db.Integer)
    date = db.Column(db.String(200))
    hour = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


# Insert user to db
def insert_user(username, email, password):
    new_user = Users(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    # basic data check, registered or not


def check_data(email):
    data = Users.query.filter_by(email=email).all()
    # data = db.select
    print(data)
    if len(data) == 0:
        return True
    else:
        return False
    # db = sq.connect("site_db")
    # cursor = db.cursor()
    # cursor.execute("""SELECT email FROM users WHERE email=(?)""", (email,))
    # data = cursor.fetchall()


def check_username(username):
    data = Users.query.filter_by(username=username).all()
    # data = sqlalchemy.select([Users.username]).where(Users.username == username)
    if len(data) == 0:
        return True
    else:
        return False
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT username FROM users WHERE username=(?)""", (username,))
    data = cursor.fetchall()
    if len(data) == 0:
        return True
    else:
        return False


def get_email(username):
    data = Users.query.filter_by(username=username).all()
    return data[0].email
    data = sqlalchemy.select([Users.email]).where(Users.username == username)
    if len(data) == 0:
        return True
    else:
        return False
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT email FROM users WHERE username=(?)""", (username,))
    data = cursor.fetchall()
    return data[0]


def get_userid(username):
    data = Users.query.filter_by(username=username).all()

    # db = sq.connect("site_db")
    # cursor = db.cursor()
    # cursor.execute("""SELECT user_id FROM users WHERE username=(?)""", (username,))
    # data = cursor.fetchall()
    return data[0].user_id


# Basic data check, using email and password to check if user entered correct login info
def check_login_data(username, password):
    data = Users.query.filter_by(username=username, password=password).all()
    # data = sqlalchemy.select([Users.username]).where(Users.username == username)
    print(type(data))
    if len(data) > 0:
        return True
    else:
        return False
    # db = sq.connect("site_db")
    # cursor = db.cursor()
    # cursor.execute("""SELECT username FROM users WHERE username=(?)""", (username,))
    # data = cursor.fetchall()
    # print(type(data))
    # if len(data) > 0:
    #     cursor.execute("""SELECT password FROM users WHERE password=(?)""", (password,))
    #     data = cursor.fetchall()
    #     print(data)
    #     if len(data) > 0:
    #         return True


# db.session.delete(modebject)
#     model.query.all()
#     students.query.filter_by(city= ’Tokyo’).all()
# insert house
def insert_house(user_id, name1, name2, lastname1, lastname2, dpi, email1, phone, address, typehome, zone, roomsnumber,
                 roomsbath, pricedol, pricequet, meters, comments, images):
    new_house = Houses(primer_nombre=name1, segundo_nombre=name2,
                       primer_apellido=lastname1, segundo_apellido=lastname2,
                       DPI=dpi, correo_electronico=email1, telefono=phone,
                       direccion=address, tipo=typehome, zona=zone, n_habitaciones=roomsnumber,
                       n_lavados=roomsbath, precio_dolares=pricedol, precio_quetzales=pricequet,
                       metros_cuadrados=meters, comentarios_adicionales=comments, user_id=user_id)
    db.session.add(new_house)
    db.session.commit()

    for image in images:
        new_image = Photos(photos=image.read(), house_id=new_house.house_id)
        db.session.add(new_image)
        db.session.commit()


def get_houses(zone, typehome, roomsnumber, roomsbath, page_number):
    data = Houses.query.filter_by(
        zona=zone, tipo=typehome, n_habitaciones=roomsnumber, n_lavados=roomsbath
    ).offset((page_number - 1) * 5).limit(5).all()
    return data
    data = sqlalchemy.select(
        [Houses.primer_nombre, Houses.segundo_nombre, Houses.primer_apellido, Houses.segundo_apellido,
         Houses.DPI, Houses.correo_electronico, Houses.telefono, Houses.direccion,
         Houses.tipo, Houses.zone, Houses.n_habitaciones, Houses.n_lavados,
         Houses.precio_dolares, Houses.precio_quetzales, Houses.metros_cuadrados, Houses.comentarios_adicionales,
         Houses.user_id, Houses.house_id]
    ).where(
        Houses.zone == zone, Houses.tipo == typehome, Houses.roomsnumber == roomsnumber, Houses.n_lavados == roomsbath
    ).offset((page_number - 1) * 5).limit(5).all()
    return data
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, DPI, correo_electronico, 
    telefono, direccion, tipo, zona, n_habitaciones, n_lavados, precio_dolares, precio_quetzales, metros_cuadrados, 
    comentarios_adicionales, user_id, house_id
    FROM houses 
    WHERE Zona=(?) AND TIPO=(?) AND n_habitaciones=(?) AND n_lavados=(?)
    LIMIT (?) 
    OFFSET (?)""",
                   (zone, typehome, roomsnumber, roomsbath, 5, (page_number - 1) * 5,))
    data = cursor.fetchall()
    return data


def remove_house(id):
    # remove house
    pass


def get_all_houses(page_number):
    data = Houses.query.offset((page_number - 1) * 5).limit(5).all()
    return data
    data = sqlalchemy.select(
        [Houses.primer_nombre, Houses.segundo_nombre, Houses.primer_apellido, Houses.segundo_apellido,
         Houses.DPI, Houses.correo_electronico, Houses.telefono, Houses.direccion,
         Houses.tipo, Houses.zone, Houses.n_habitaciones, Houses.n_lavados,
         Houses.precio_dolares, Houses.precio_quetzales, Houses.metros_cuadrados,
         Houses.comentarios_adicionales,
         Houses.user_id, Houses.house_id]
    ).offset((page_number - 1) * 5).limit(5).all()
    return data
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, DPI, correo_electronico, 
    telefono, direccion, tipo, zona, n_habitaciones, n_lavados, precio_dolares, precio_quetzales, metros_cuadrados, 
    comentarios_adicionales, user_id, house_id
    FROM houses 
    LIMIT (?) 
    OFFSET (?)""",
                   (5, (page_number - 1) * 5,))
    data = cursor.fetchall()
    return data


def get_house_images(house_id, num_image):
    data = Photos.query.filter_by(house_id=house_id).offset(int(num_image) - 1).limit(1).all()
    return data
    print(num_image, house_id)
    data = sqlalchemy.select(
        [Photos.photos]
    ).where(
        Photos.house_id == house_id
    ).offset(int(num_image) - 1).limit(1).all()
    return data[0]
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT photos
    FROM photos 
    WHERE house_id=(?)
    LIMIT 1 OFFSET (?)""",
                   (int(house_id), int(num_image) - 1,))
    data = cursor.fetchall()
    return data[0]


def insert_cita(user_id, name3, name4, lastname3, lastname4, dpi1, email2, phone1, date, hour):
    new_cita = Citas(user_id=user_id, name3=name3, name4=name4, lastname3=lastname3, lastname4=lastname4, dpi1=dpi1,
                     email2=email2, phone1=phone1, date=date, hour=hour)
    db.session.add(new_cita)
    db.session.commit()
# def create():
#     db = sq.connect("site_db")
#     cursor = db.cursor()
#     print("creating database connection file!")
#     time.sleep(1)
#     # creating users table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS
#         users(
#             user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#             username TEXT,
#             email TEXT,
#             password BLOB)
#         """)
#     # creating houses table
#     cursor.execute("""
#             CREATE TABLE IF NOT EXISTS
#             houses(
#                 house_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                 primer_nombre TEXT,
#                 segundo_nombre TEXT,
#                 primer_apellido TEXT,
#                 segundo_apellido TEXT,
#                 DPI INTEGER,
#                 correo_electronico TEXT,
#                 telefono NUMERIC,
#                 direccion TEXT,
#                 tipo TEXT,
#                 zona NUMERIC,
#                 n_habitaciones NUMERIC,
#                 n_lavados NUMERIC,
#                 precio_dolares FLOAT,
#                 precio_quetzales FLOAT,
#                 metros_cuadrados FLOAT,
#                 comentarios_adicionales TEXT,
#                 user_id INTEGER,
#                 FOREIGN KEY (user_id) REFERENCES user (user_id))
#             """)
#     # create photos table
#     cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS
#                 photos(
#                     photos_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                     photos BLOB NOT NULL,
#                     house_id INTEGER,
#                     FOREIGN KEY (house_id) REFERENCES houses (house_id))
#                 """)
#
#     db.commit()
