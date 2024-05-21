from flask import Blueprint, flash, url_for, redirect, render_template
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from src.views import menu

from src.database import db
from src.users.forms import RegistrForm, LoginForm
from src.users.models import User

signup_user_page = Blueprint('signup_user_page', __name__)
logout_page = Blueprint('logout_page', __name__)
signin_user_page = Blueprint('signin_user_page', __name__)


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
