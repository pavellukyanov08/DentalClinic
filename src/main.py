import logging
import os
from flask import Flask
from views import main_page, add_client_page
from src.database import Config, db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sqlalchemy.engine')

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(main_page)
app.register_blueprint(add_client_page)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
