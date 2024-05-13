from flask import render_template, request, redirect, url_for, Blueprint, flash
from sqlalchemy import insert

from src.clinic.forms import ClientForm
from src.database import db
from src.clinic.models import Client, PlaceResidence

menu = [
    {'name': 'База клиентов', 'url': '/'},
    {'name': 'Добавить клиента', 'url': 'add_client'},
]

clients_base = Blueprint('clients_base', __name__)
add_client_page = Blueprint('add_client_page', __name__)
update_client_page = Blueprint('update_client_page', __name__)
delete_client_page = Blueprint('delete_client_page', __name__)


@clients_base.route('/')
def index():
    clients = Client.query.order_by(Client.id)
    return render_template('clients_base.html',
                           title='Главная страница',
                           menus=menu,
                           clients=clients)


@add_client_page.route('/add_client', methods=['GET', 'POST'])
def add_client():
    form = ClientForm()
    if form.validate_on_submit():
        # проверка наличие места прописки
        residence = PlaceResidence.query.filter_by(city=form.city.data,
                                                   street_name=form.street.data,
                                                   house_num=form.house_num.data,
                                                   apartment_num=form.apartment_num.data,
                                                   ).first()

        if not residence:
            residence = PlaceResidence(city=form.city.data,
                                       street_name=form.street.data,
                                       house_num=form.house_num.data,
                                       apartment_num=form.apartment_num.data,
                                       )
            db.session.add(residence)
            db.session.flush()

        client = Client(fullname=form.fullname.data,
                        birthday=form.birthday.data,
                        gender=form.gender.data,
                        phone=form.phone.data,
                        place_residence = residence,
                        )

        db.session.add(client)
        db.session.commit()
        flash('Client added successfully!')

        return redirect(url_for('clients_base.index'))
    return render_template('add_client.html', menus=menu, form=form)


@update_client_page.route('/update/<int:idx>', methods=['GET', 'POST'])
def update_client(idx):
    client = Client.query.get_or_404(idx)
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        client.fullname = form.fullname.data
        client.birthday = form.birthday.data
        client.gender = form.gender.data
        client.phone = form.phone.data

        client.city = form.city.data
        client.street = form.city.data
        client.house_num = form.city.data
        client.apartment_num = form.city.data
        db.session.commit()
        flash('Client added successfully!')
        return redirect(url_for('clients_base.index'))
    return render_template('update_client.html', menus=menu, form=form)


@delete_client_page.route('/delete/<int:idx>', methods=['POST'])
def delete_client(idx):
    client = Client.query.get_or_404(idx)
    db.session.delete(client)
    db.session.commit()
    flash('Client added successfully!')
    return redirect(url_for('clients_base.index'))
