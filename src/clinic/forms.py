from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Regexp


class ClientForm(FlaskForm):
    fullname = StringField("ФИО", validators=[DataRequired()])
    birthday = DateField("Дата рождения", format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField("Пол", choices=[('мужской', 'Мужской'), ('женский', 'Женский')], validators=[DataRequired()])
    phone = StringField("Номер телефона", validators=[DataRequired()])

    # Адрес прописки
    city = StringField("Город", validators=[DataRequired()])
    street = StringField("Улица", validators=[DataRequired()])
    house_num = StringField("Номер дома", validators=[DataRequired()])
    apartment_num = StringField("Квартира", validators=[DataRequired()])

    registered_at = DateField('Дата регистрации', format='%Y-%m-%d', default=date.today(), validators=[DataRequired()])

    submit = SubmitField("Зарегистрировать клиента")
    update = SubmitField("Обновить данные")
    delete = SubmitField("Удалить клиента из базы")