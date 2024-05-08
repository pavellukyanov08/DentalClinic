from flask import render_template, request, redirect, url_for, Blueprint, flash

from src.clinic.forms import AddClientForm
from src.database import db
from src.clinic.models import Client

menu = [
    {'name': 'Главная', 'url': '/'},
    {'name': 'База клиентов', 'url': 'clients'},
    {'name': 'Добавить клиента', 'url': 'add_client'},
]

main_page = Blueprint('main_page', __name__)
# get_clients = Blueprint('get_clients', __name__)
add_client_page = Blueprint('add_client_page', __name__)


@main_page.route('/')
def index():
    return render_template('main_page.html', title='Главная страница', menus=menu)


@add_client_page.route('/add_client', methods=['GET', 'POST'])
def add_client():
    form = AddClientForm()
    if form.validate_on_submit():
        new_client = Client(fullname=form.fullname.data,
                            birthday=form.birthday.data,
                            gender=form.gender.data,
                            place_residence=form.place_residence.data,
                            phone=form.phone.data,
                            )
        db.session.add(new_client)
        db.session.commit()
        flash('Client added successfully!')
    return render_template('add_client.html', menus=menu, form=form)