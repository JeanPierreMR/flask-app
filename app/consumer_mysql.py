from kafka import KafkaConsumer
from json import loads
from time import sleep

from sqlalchemy import create_engine
db = create_engine('sqlite:///site_db')

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



consumer = KafkaConsumer(
    'topic_mysql',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)


#------------------------INSERTS------------------------
#producer.send('topic_mysql', value=data)
#producer.send('topic_es', value=data)
def insert_cita(user_id, name3, name4, lastname3, lastname4, dpi1, email2, phone1, date, hour, comments):
    new_cita = Citas(user_id=user_id, name3=name3, name4=name4, lastname3=lastname3, lastname4=lastname4, dpi1=dpi1,
                     email2=email2, phone1=phone1, date=date, hour=hour)
    db.session.add(new_cita)
    db.session.commit()


# Insert user to db
def insert_user(username, email, password):
    new_user = Users(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

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

#delete
def remove_house(id):
    data = Houses.query.filter_by(house_id=id).delete()

db_actions = {
    'insert_cita': insert_cita,
    'insert_user': insert_user,
    'insert_house': insert_house,
    'remove_house': remove_house
}



for event in consumer:
    data_dict = event.value
    db_actions[data_dict['op']]()

