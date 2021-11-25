import sqlite3 as sq
import time
from elasticsearch import Elasticsearch
import sqlalchemy
from kafka import KafkaConsumer, KafkaProducer

from json import loads
from json import dumps
from app import db as db

# connect to our cluster Elastic Search
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.delete(index='houses_index', ignore=[400, 404])
es.indices.delete(index='citas_index', ignore=[400, 404])

# KAFKA Conections
Kafka_server = "localhost:9092"
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)


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
    DPI = db.Column(db.BigInteger)
    correo_electronico = db.Column(db.String(200))
    telefono = db.Column(db.BigInteger)
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
    photos = db.Column(db.LargeBinary(length=541618))
    # house_id = db.Column(db.BigInteger)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.house_id'))


class Citas(db.Model):
    __tablename__ = "citas"
    cita_id = db.Column(db.Integer, primary_key=True)
    name3 = db.Column(db.String(200))
    name4 = db.Column(db.String(200))
    lastname3 = db.Column(db.String(200))
    lastname4 = db.Column(db.String(200))
    dpi1 = db.Column(db.BigInteger)
    email2 = db.Column(db.String(200))
    phone1 = db.Column(db.BigInteger)
    date = db.Column(db.String(200))
    hour = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


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


def get_houses(zone, typehome, roomsnumber, roomsbath, page_number):
    data = Houses.query.filter_by(
        zona=zone, tipo=typehome, n_habitaciones=roomsnumber, n_lavados=roomsbath
    ).offset((page_number - 1) * 5).limit(5).all()
    print(f"data> {data}")
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


def search_houses(query):
    result = es.search(index="houses_index",
                       body={"query": {
                           "match": {
                               "comment": query,
                           }}
                       })
    x = 0
    houses = []
    for doc in result['hits']['hits']:
        if x == 5:
            break
        x += 1
        id = doc['_source']['id']
        data = Houses.query.filter_by(house_id=id).all()
        try:
            houses.append(data[0])
        except:
            print("index change to db")
            pass
    return houses


def search_cita(query):
    result = es.search(index="citas_index",
                       body={"query": {
                           "match": {
                               "comment": query,
                           }}
                       })
    x = 0
    citas = []
    for doc in result['hits']['hits']:
        if x == 5:
            break
        x += 1
        id = doc['_source']['id']
        data = Citas.query.filter_by(cita_id=id).all()
        try:
            citas.append(data[0])
        except:
            print("index change to dbcitas")
            pass
    return citas


# ------------------------INSERTS------------------------
# producer.send('topic_mysql', value=data)
# producer.send('topic_es', value=data)
def insert_cita(user_id, name3, name4, lastname3, lastname4, dpi1, email2, phone1, date, hour, comments):
    data_dict = {
        'op': 'insert_cita',
        'user_id': user_id,
        'name3': name3,
        'name4': name4,
        'lastname3': lastname3,
        'lastname4': lastname4,
        'dpi1': dpi1,
        'email2': email2,
        'phone1': phone1,
        'date': date,
        'hour': hour,
        'comments': comments
    }
    producer.send('topic_mysql', value=data_dict)
    # new_cita = Citas(user_id=user_id, name3=name3, name4=name4, lastname3=lastname3, lastname4=lastname4, dpi1=dpi1,
    #                  email2=email2, phone1=phone1, date=date, hour=hour)
    # db.session.add(new_cita)
    # db.session.commit()

    data = {'comment': comments, 'id': new_cita.cita_id}
    producer.send('topic_es', value=data)
    # es.index(index='citas_index', id=new_cita.cita_id,
    #          body={'comment': comments, 'id': new_cita.cita_id})


# Insert user to db
def insert_user(username, email, password):
    data_dict = {
        'op': 'insert_user',
        'username': username,
        'email': email,
        'password': password
    }
    producer.send('topic_mysql', value=data_dict)
    # new_user = Users(username=username, email=email, password=password)
    # db.session.add(new_user)
    # db.session.commit()


def insert_house(user_id, name1, name2, lastname1, lastname2, dpi, email1, phone, address, typehome, zone, roomsnumber,
                 roomsbath, pricedol, pricequet, meters, comments, images):
    # data_dict = {
    #     'op': 'insert_house',
    #     'user_id': user_id,
    #     'name1': name1,
    #     'name2': name2,
    #     'lastname1': lastname1,
    #     'lastname2': lastname2,
    #     'dpi': dpi,
    #     'email1': email1,
    #     'phone': phone,
    #     'address': address,
    #     'typehome': typehome,
    #     'zone': zone,
    #     'roomsnumber': roomsnumber,
    #     'roomsbath': roomsbath,
    #     'pricedol': pricedol,
    #     'pricequet': pricequet,
    #     'meters': meters,
    #     'comments': comments,
    #     'images': images
    # }
    # producer.send('topic_mysql', value=data_dict)
    new_house = Houses(primer_nombre=name1, segundo_nombre=name2,
                       primer_apellido=lastname1, segundo_apellido=lastname2,
                       DPI=dpi, correo_electronico=email1, telefono=phone,
                       direccion=address, tipo=typehome, zona=zone, n_habitaciones=roomsnumber,
                       n_lavados=roomsbath, precio_dolares=pricedol, precio_quetzales=pricequet,
                       metros_cuadrados=meters, comentarios_adicionales=comments, user_id=user_id)
    db.session.add(new_house)
    db.session.commit()

    data = {'comment': comments, 'id': new_house.house_id}
    producer.send('topic_es', value=data)
    es.index(index='houses_index', id=new_house.house_id,
             body={'comment': comments,
                   'id': new_house.house_id,
                   'typehome': typehome,
                    'zone': zone,
                    'roomsnumber': roomsnumber,
                    'roomsbath': roomsbath,
                    'pricedol': pricedol,
                    'pricequet': pricequet
                   })


    for image in images:
        new_image = Photos(photos=image.read(), house_id=new_house.house_id)
        db.session.add(new_image)
        db.session.commit()
        #insert_image


# delete
def remove_house(id):
    data_dict = {
        'op': 'remove_house',
        'id': id
    }
    producer.send('topic_mysql', value=data_dict)
    es.delete(index="houses_index", id=id)
    # data = Houses.query.filter_by(house_id=id).delete()
