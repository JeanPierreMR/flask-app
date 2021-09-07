from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, RadioField, TextAreaField, SubmitField, FloatField, FileField
from wtforms.validators import Required
from flask_wtf import Form
from wtforms.validators import InputRequired, Email, DataRequired
from flask_wtf.file import FileAllowed, FileRequired

class LoginForma(FlaskForm):
    user = TextField(u'Usuario', validators=[Required()])
    password = PasswordField(u'Contraseña', validators=[Required()])


class registration_forma(Form):
    name = TextField(label="Username", validators=[DataRequired()])
    password = PasswordField(label=" Password ", validators=[DataRequired()])
    phoneNumber = IntegerField(labe1="Enter mobile number", validators=[DataRequired()])
    gender = RadioField('Gender', choices=['Male', ' Female'])
    address = TextAreaField(label=" Address ")
    age = IntegerField(label="Age")
    submit = SubmitField("Send")


class LoginForm(FlaskForm):
    username = TextField('Username', id='username_login', validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username', id='username_create', validators=[DataRequired()])
    email = TextField('Email', id='email_create', validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_create', validators=[DataRequired()])


class VentaForm(FlaskForm):
    name1 = TextField('primer_nombre', id='primer_nombre_create', validators=[DataRequired()])
    name2 = TextField('segundo_nombre', id='segundo_nombre_create', validators=[DataRequired()])
    lastname1 = TextField('primer_apellido', id='primer_apellido_create', validators=[DataRequired()])
    lastname2 = TextField('segundo_apellido', id='segundo_apellido_create', validators=[DataRequired()])
    dpi = IntegerField('DPI', id='DPI_create', validators=[DataRequired()])
    email1 = TextField('correo_electronico', id='correo_electronico_create', validators=[DataRequired()])
    phone = IntegerField('telefono', id='telefono_create', validators=[DataRequired()])
    address = TextField('direccion', id='direccion_create', validators=[DataRequired()])
    typehome = TextField('tipo', id='tipo_create', validators=[DataRequired()])
    zone = IntegerField('zona', id='zona_create', validators=[DataRequired()])
    roomsnumber = IntegerField('n_habitaciones', id='n_habitaciones_create', validators=[DataRequired()])
    roomsbath = IntegerField('n_banos', id='n_banos_create', validators=[DataRequired()])
    pricedol = FloatField('precio_dolares', id='precio_dolares_create', validators=[DataRequired()])
    pricequet = FloatField('precio_quetzales', id='precio_quetzales_create', validators=[DataRequired()])
    meters = FloatField('metros_cuadrados', id='metros_cuadrados_create', validators=[DataRequired()])
    comments = TextField('comentarios_adicionales', id='comentarios_adicionales_create', validators=[DataRequired()])
    photos = FileField(u'photos', id='photos_create', validators=[
        FileRequired(),
        FileAllowed(['png', 'jpg'], "wrong format!")
    ])
    # photos = FileField(u'photos', id='photos_create', validators=[regexp('^[^/\\]\.jpg$')])
    submit = SubmitField("Send")
