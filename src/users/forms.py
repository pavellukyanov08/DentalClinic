from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, EqualTo, Email


class UserForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired()])
    fullname = StringField("ФИО", validators=[DataRequired()])
    hash_password = PasswordField("Пароль", validators=[DataRequired(), EqualTo('hash_password_confirm', message='Пароли должны совподать!')])
    hash_password_confirm = PasswordField("Подтверждение пароля", validators=[DataRequired()])

    registered_at = DateField('Дата регистрации', format='%Y-%m-%d', default=date.today(), validators=[DataRequired()])

    def __repr__(self):
        return f"Пользователь: {self.email}. ФИО: {self.fullname}"


class LoginForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
