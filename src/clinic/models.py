from datetime import datetime
from src.database import db


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    place_residence = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    med_card = db.Column(db.String(1000), nullable=True)

    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Клиент № {self.id}: ФИО: {self.fullname}"