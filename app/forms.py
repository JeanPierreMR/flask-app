from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, RadioField, TextAreaField, SubmitField
from wtforms.validators import Required
from flask_wtf import Form
from wtforms.validators import InputRequired, Email, DataRequired


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
