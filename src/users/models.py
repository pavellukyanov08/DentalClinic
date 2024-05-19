from datetime import datetime

from flask_login import UserMixin

from src.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    fullname = db.Column(db.String(100), nullable=False)
    hash_password = db.Column(db.String(256), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readably attribute!')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)

    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
