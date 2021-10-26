from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, RadioField, TextAreaField, SubmitField, FloatField, \
    FileField, SelectField, MultipleFileField
from wtforms.validators import Required, StopValidation
from flask_wtf import Form
from wtforms.validators import InputRequired, Email, DataRequired
from flask_wtf.file import FileAllowed, FileRequired
from collections import Iterable
from werkzeug.datastructures import FileStorage


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


class MultiFileAllowed(object):

    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):

        # FileAllowed only expects a single instance of FileStorage
        # if not (isinstance(field.data, FileStorage) and field.data):
        #     return

        # Check that all the items in field.data are FileStorage items
        if not (all(isinstance(item, FileStorage) for item in field.data) and field.data):
            return

        for data in field.data:
            filename = data.filename.lower()

            if isinstance(self.upload_set, Iterable):
                if any(filename.endswith('.' + x) for x in self.upload_set):
                    return

                raise StopValidation(self.message or field.gettext(
                    'File does not have an approved extension: {extensions}'
                ).format(extensions=', '.join(self.upload_set)))

            if not self.upload_set.file_allowed(field.data, filename):
                raise StopValidation(self.message or field.gettext(
                    'File does not have an approved extension.'
                ))


class VentaForm(FlaskForm):
    name1 = TextField('primer_nombre', id='primer_nombre_create', validators=[DataRequired()])
    name2 = TextField('segundo_nombre', id='segundo_nombre_create', validators=[DataRequired()])
    lastname1 = TextField('primer_apellido', id='primer_apellido_create', validators=[DataRequired()])
    lastname2 = TextField('segundo_apellido', id='segundo_apellido_create', validators=[DataRequired()])
    dpi = IntegerField('DPI', id='DPI_create', validators=[DataRequired()])
    email1 = TextField('correo_electronico', id='correo_electronico_create', validators=[DataRequired()])
    phone = IntegerField('telefono', id='telefono_create', validators=[DataRequired()])
    address = TextField('direccion', id='direccion_create', validators=[DataRequired()])
    typehome = SelectField('Tipo', choices=[('Apartamento', 'Apartamento'), ('Casa', 'Casa')])
    zone = SelectField('Zona', choices=[('9', '9'), ('10', '10'), ('14', '14'), ('15', '15'), ('16', '16')])
    roomsnumber = SelectField('Habitaciones', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    roomsbath = SelectField('Baños', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    pricedol = FloatField('precio_dolares', id='precio_dolares_create', validators=[DataRequired()])
    pricequet = FloatField('precio_quetzales', id='precio_quetzales_create', validators=[DataRequired()])
    meters = FloatField('metros_cuadrados', id='metros_cuadrados_create', validators=[DataRequired()])
    comments = TextField('comentarios_adicionales', id='comentarios_adicionales_create', validators=[DataRequired()])
    images = MultipleFileField(
        'file',
        validators=[
            InputRequired(),
            MultiFileAllowed(['jpg', 'png', 'jpeg', 'tif'])
        ]
    )

    # photos = FileField(u'photos', id='photos_create', validators=[regexp('^[^/\\]\.jpg$')])
    submit = SubmitField("Enviar")


class CompraForm(FlaskForm):
    zone = SelectField('Zona', choices=[('9', '9'), ('10', '10'), ('14', '14'), ('15', '15'), ('16', '16')])
    typehome = SelectField('Tipo', choices=[('Apartamento', 'Apartamento'), ('Casa', 'Casa')])
    roomsnumber = SelectField('Habitaciones', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    roomsbath = SelectField('Baños', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    submit = SubmitField("Buscar")


class CitaForm(FlaskForm):
    name3 = TextField('primer_nombre', id='primer_nombre_create', validators=[DataRequired()])
    name4 = TextField('segundo_nombre', id='segundo_nombre_create', validators=[DataRequired()])
    lastname3 = TextField('primer_apellido', id='primer_apellido_create', validators=[DataRequired()])
    lastname4 = TextField('segundo_apellido', id='segundo_apellido_create', validators=[DataRequired()])
    dpi1 = IntegerField('DPI', id='DPI_create', validators=[DataRequired()])
    email2 = TextField('correo_electronico', id='correo_electronico_create', validators=[DataRequired()])
    phone1 = IntegerField('telefono', id='telefono_create', validators=[DataRequired()])
    date = SelectField('Calendario', choices=[('10 de noviembre', '10 de noviembre'), ('11 de noviembre', '11 de noviembre'),('12 de noviembre','12 de noviembre')])
    hour = SelectField('Horario', choices=[('1', '1'), ('3', '3'), ('4', '4')])

    submit = SubmitField("Enviar")


