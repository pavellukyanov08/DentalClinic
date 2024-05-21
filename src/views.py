from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.clinic.forms import ClientForm, DoctorForm, AppointmentForm
from src.database import db
from src.clinic.models import (
    Client,
    PlaceResidence,
    Specialization,
    Doctor,
    Appointment,
)
from src.users.models import User, Role
from src.users.forms import UserForm, LoginForm, RegistrForm

menu = [
    {'name': 'База клиентов', 'url': '/clients'},
    {'name': 'База врачей', 'url': '/doctors'},

    {'name': 'Добавить клиента', 'url': '/add_client'},
    {'name': 'Добавить врача', 'url': '/add_doctor'},

    {'name': 'Регистрация', 'url': '/signup'},
    {'name': 'Авторизация', 'url': '/signin'},
    {'name': 'Выйти', 'url': '/logout'},
]

# nav_menu = menu[:4]
# auth_menu = menu[4:]

clients_base = Blueprint('clients_base', __name__)
doctors_base = Blueprint('doctors_base', __name__)

add_client_page = Blueprint('add_client_page', __name__)
book_appointment_page = Blueprint('book_appointment_page', __name__)
appointments_list = Blueprint('appointments_list', __name__)
delete_appointment_page = Blueprint('delete_appointment_page', __name__)


add_doctor_page = Blueprint('add_doctor_page', __name__)

update_client_page = Blueprint('update_client_page', __name__)
update_doctor_page = Blueprint('update_doctor_page', __name__)

delete_client_page = Blueprint('delete_client_page', __name__)
delete_doctor_page = Blueprint('delete_doctor_page', __name__)

signup_user_page = Blueprint('signup_user_page', __name__)
logout_page = Blueprint('logout_page', __name__)
signin_user_page = Blueprint('signin_user_page', __name__)


@clients_base.route('/clients', methods=['GET'])
@login_required
def get_clients():
    clients = Client.query.order_by(Client.id)
    return render_template('registrator/clients_base.html',
                           title='Главная страница',
                           menus=menu,
                           clients=clients)


@doctors_base.route('/doctors', methods=['GET'])
@login_required
def get_doctors():
    doctors = Doctor.query.order_by(Doctor.id)
    return render_template('registrator/doctors_base.html',
                           title='Главная страница',
                           menus=menu,
                           doctors=doctors)


@add_client_page.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    client_form = ClientForm()

    if client_form.validate_on_submit():
        # проверка наличия места прописки
        residence = PlaceResidence.query.filter_by(city=client_form.city.data,
                                                   street_name=client_form.street.data,
                                                   house_num=client_form.house_num.data,
                                                   apartment_num=client_form.apartment_num.data,
                                                   ).first()

        if not residence:
            residence = PlaceResidence(city=client_form.city.data,
                                       street_name=client_form.street.data,
                                       house_num=client_form.house_num.data,
                                       apartment_num=client_form.apartment_num.data,
                                       )
            db.session.add(residence)
            db.session.flush()

        client = Client(fullname=client_form.fullname.data,
                        birthday=client_form.birthday.data,
                        gender=client_form.gender.data,
                        phone=client_form.phone.data,
                        place_residence=residence,
                        )

        db.session.add(client)
        db.session.commit()
        flash('Client added successfully!')

        return redirect(url_for('clients_base.get_clients'))
    return render_template('registrator/add_client.html', menus=menu, client_form=client_form)


@book_appointment_page.route('/add_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    appointment_form = AppointmentForm()

    clients = Client.query.with_entities(Client.id, Client.fullname).all()
    appointment_form.client_name.choices = [(client.id, client.fullname) for client in clients]

    doctors = Doctor.query.with_entities(Doctor.id, Doctor.fullname).all()
    appointment_form.doctor_name.choices = [(doctor.id, doctor.fullname) for doctor in doctors]

    if appointment_form.validate_on_submit():
        client_id = appointment_form.client_name.data
        doctor_id = appointment_form.doctor_name.data
        appointment_date = appointment_form.date_appointment.data
        appointment_time = appointment_form.time_appointment.data

        # Здесь вы можете сохранить запись в базе данных
        appointment = Appointment(
            client_id=client_id,
            doctor_id=doctor_id,
            date=appointment_date,
            time=appointment_time
        )
        db.session.add(appointment)
        db.session.commit()
        # flash('Client added successfully!')

        return redirect(url_for('clients_base.get_clients'))
    return render_template('registrator/add_appointment.html', menus=menu, appointment_form=appointment_form)


@appointments_list.route('/appointments', methods=['GET'])
@login_required
def get_appointments():
    appointments = Appointment.query.order_by(Appointment.date).all()
    return render_template('registrator/appointments_base.html', appointments=appointments)


@delete_appointment_page.route('/delete_apnt/<int:idx>', methods=['POST'])
@login_required
def delete_appointment(idx):
    appointment = Appointment.query.get_or_404(idx)

    db.session.delete(appointment)
    db.session.commit()

    flash('Client deleted successfully!')
    return redirect(url_for('appointments_list.get_appointments'))



@add_doctor_page.route('/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    doctor_form = DoctorForm()
    if doctor_form.validate_on_submit():
        # проверка наличие места прописки
        specialization = Specialization.query.filter_by(name=doctor_form.specialization.data).first()

        if not specialization:
            specialization = Specialization(
                name=doctor_form.specialization.data
            )

            db.session.add(specialization)
            db.session.flush()

        doctor = Doctor(fullname=doctor_form.fullname.data,
                        gender=doctor_form.gender.data,
                        phone=doctor_form.phone.data,
                        specialization=specialization,
                        )

        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added successfully!')

        return redirect(url_for('doctors_base.get_doctors'))
    return render_template('registrator/add_doctor.html', menus=menu, doctor_form=doctor_form)


@update_client_page.route('/update_cl/<int:idx>', methods=['GET', 'POST'])
@login_required
def update_client(idx):
    client = Client.query.get_or_404(idx)
    client_form = ClientForm(obj=client)

    if request.method == 'GET':
        if client.place_residence:
            client_form.city.data = client.place_residence.city
            client_form.street.data = client.place_residence.street_name
            client_form.house_num.data = client.place_residence.house_num
            client_form.apartment_num.data = client.place_residence.apartment_num

    if client_form.validate_on_submit():
        client.fullname = client_form.fullname.data
        client.birthday = client_form.birthday.data
        client.gender = client_form.gender.data
        client.phone = client_form.phone.data

        if client.place_residence:
            client.place_residence.city = client_form.city.data
            client.place_residence.street_name = client_form.street.data
            client.place_residence.house_num = client_form.house_num.data
            client.place_residence.apartment_num = client_form.apartment_num.data
        else:
            new_residence = PlaceResidence(
                city=client_form.city.data,
                street_name=client_form.street.data,
                house_num=client_form.house_num.data,
                apartment_num=client_form.apartment_num.data
            )
            db.session.add(new_residence)
            client.place_residence = new_residence

        db.session.commit()
        flash('Client updated successfully!')

        return redirect(url_for('clients_base.get_clients'))

    return render_template('registrator/client_detail.html', menus=menu, client_form=client_form)


@delete_client_page.route('/delete_cl/<int:idx>', methods=['POST'])
@login_required
def delete_client(idx):
    client = Client.query.get_or_404(idx)
    print(client)

    db.session.delete(client)
    db.session.commit()

    flash('Client deleted successfully!')
    return redirect(url_for('clients_base.get_clients'))


@update_doctor_page.route('/update_doc/<int:idx>', methods=['GET', 'POST'])
@login_required
def update_doctor(idx):
    doctor = Doctor.query.get_or_404(idx)
    doctor_form = DoctorForm(obj=doctor)

    if request.method == 'GET':
        if doctor_form.specialization:
            doctor_form.specialization.data = doctor_form.specialization.name

    if doctor_form.validate_on_submit():
        doctor_form.fullname = doctor_form.fullname.data
        doctor_form.gender = doctor_form.gender.data
        doctor_form.phone = doctor_form.phone.data

        if doctor.specialization:
            doctor.specialization.name = doctor_form.specialization.data
        else:
            new_specialization = Specialization(
                name=doctor_form.specialization.data
            )
            db.session.add(new_specialization)
            doctor.place_residence = new_specialization

        db.session.commit()
        flash('Doctor updated successfully!')

        return redirect(url_for('doctors_base.get_doctors'))

    return render_template('registrator/doctor_detail.html', menus=menu, doctor_form=doctor_form)


@delete_doctor_page.route('/delete_doc/<int:idx>', methods=['POST'])
@login_required
def delete_doctor(idx):
    doctor = Doctor.query.get_or_404(idx)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted successfully!')
    return redirect(url_for('doctors_base.get_doctors'))


# Authentification
@signup_user_page.route('/signup', methods=['GET', 'POST'])
def signup_user():
    signup_form = RegistrForm()

    if signup_form.validate_on_submit():
        user = User.query.filter_by(email=signup_form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(signup_form.hash_password.data)
            user = User(email=signup_form.email.data,
                        fullname=signup_form.fullname.data,
                        hash_password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрированы!')

        return redirect(url_for('clients_base.get_clients'))
    return render_template('auth/registr.html', menus=menu, signup_form=signup_form)


@signin_user_page.route('/signin', methods=['GET', 'POST'])
def signin_user():
    signin_form = LoginForm()

    if signin_form.validate_on_submit():
        user = User.query.filter_by(email=signin_form.email.data).first()
        if user:
            if check_password_hash(user.hash_password, signin_form.password.data):
                login_user(user)
                flash('Вы авторизованы!')
                return redirect(url_for('clients_base.get_clients'))
            else:
                flash("Неверное имя пользователя или пароль!")
        else:
            flash("Пользователь не найден!")

        return redirect(url_for('clients_base.get_clients'))
    return render_template('auth/authoriz.html', menus=menu, signin_form=signin_form)


@logout_page.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Вы вышли из профиля")
    return redirect(url_for('signin_user_page.signin_user'))
