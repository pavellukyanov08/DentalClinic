import logging
import os
from flask import Flask, render_template
from views import clients_base, add_client_page, update_client_page, delete_client_page
from src.database import Config, db
from flask_migrate import Migrate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sqlalchemy.engine')

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config.from_object(Config)
db.init_app(app)

migrate = Migrate(app, db, directory='src/migrations')

app.register_blueprint(clients_base)
app.register_blueprint(add_client_page)
app.register_blueprint(update_client_page)
app.register_blueprint(delete_client_page)


# Errors pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors_pages/404.html'), 404


@app.errorhandler(505)
def page_not_found(e):
    return render_template('errors_pages/505.html'), 505


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
