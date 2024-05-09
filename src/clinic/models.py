from datetime import datetime
from src.database import db


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    place_residence = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    med_card = db.Column(db.String(1000), nullable=True)

    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Клиент № {self.id}: ФИО: {self.fullname}"


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)