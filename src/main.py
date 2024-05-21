import logging
import os
from flask import Flask, render_template, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_required

from src.clinic.models import Doctor, Client
from src.users.models import User, Role
from src.views import (clients_base,
                       doctors_base,
                       add_client_page,
                       book_appointment_page,
                       appointments_list,
                       add_doctor_page,
                       update_client_page,
                       update_doctor_page,
                       delete_client_page,
                       delete_doctor_page,
                       signup_user_page,
                       signin_user_page,
                       logout_page, delete_appointment_page,
                       )
from src.admin.views import (
    admin_page,
    update_user_page,
    delete_user_page,
)
from src.database import Config, db
from flask_migrate import Migrate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sqlalchemy.engine')

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config.from_object(Config)
db.init_app(app)

migrate = Migrate(app, db, directory='src/migrations')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin_user_page.signin_user'

admin = Admin(app, name='DentalClinic', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))

admin.add_view(ModelView(Client, db.session))
admin.add_view(ModelView(Doctor, db.session))


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


app.register_blueprint(admin_page)
app.register_blueprint(update_user_page)
app.register_blueprint(delete_user_page)

app.register_blueprint(clients_base)
app.register_blueprint(doctors_base)

app.register_blueprint(add_client_page)
app.register_blueprint(book_appointment_page)
app.register_blueprint(appointments_list)
app.register_blueprint(delete_appointment_page)

app.register_blueprint(add_doctor_page)

app.register_blueprint(update_client_page)
app.register_blueprint(update_doctor_page)

app.register_blueprint(delete_client_page)
app.register_blueprint(delete_doctor_page)

app.register_blueprint(signup_user_page)
app.register_blueprint(signin_user_page)
app.register_blueprint(logout_page)


@app.route('/')
@login_required
def index():
    return redirect(url_for('clients_base.get_clients'))


# Errors pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors_pages/404.html'), 404


@app.errorhandler(505)
def page_not_found(e):
    return render_template('errors_pages/505.html'), 505


if __name__ == '__main__':
    app.run(debug=True)
