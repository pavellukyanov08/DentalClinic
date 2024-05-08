from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///clients.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()