from datetime import datetime
from src.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    # place_residence = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    med_card = db.Column(db.String(1000), nullable=True)

    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    place_residence_id = db.Column(db.Integer, db.ForeignKey("place_residence.id"), nullable=False)
    place_residence = db.relationship(
        'PlaceResidence',
        back_populates='clients'
    )

    def __repr__(self):
        return f"Клиент № {self.id}: ФИО: {self.fullname}"


class PlaceResidence(db.Model):
    __tablename__ = 'place_residence'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(50), nullable=False)
    street_name = db.Column(db.String(100), nullable=False)
    house_num = db.Column(db.Integer, nullable=False)
    apartment_num = db.Column(db.Integer, nullable=False)

    clients = db.relationship(
        'Client',
        back_populates='place_residence', cascade="all, delete-orphan"
    )


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    specialization_id = db.Column(db.ForeignKey("specializations.id"), nullable=False)

    appointments = db.relationship(
        'Appointment',
        back_populates='doctor'
    )

    specialization = db.relationship(
        'Specialization',
        back_populates='doctors',
    )


class Specialization(db.Model):
    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    doctors = db.relationship(
        'Doctor',
        back_populates='specialization'
    )


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    doctor = db.relationship(
        'Doctor',
        back_populates='appointments'
    )

# class Role(db.Model):
#     __tablename__ = 'roles'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(50), nullable=False)
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), nullable=False)
#     hash_password = db.Column(db.String(128), nullable=False)
#
#     @property
#     def password(self):
#         raise AttributeError('password is not a readably attribute!')
#
#     @password.setter
#     def password(self, password):
#         self.hash_password = generate_password_hash(password)
#
#     def verify_password(self, password):
#         return check_password_hash(self.hash_password, password)
#
#     registered_at = db.Column(db.DateTime, default=datetime.utcnow)
#
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
