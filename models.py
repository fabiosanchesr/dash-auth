from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
import database as db


Base = declarative_base()

class Users(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id):
        return users.get(user_id)

user = db.session.query(Users).filter_by(username='fab%').first()

#Base.metadata.create_all(db.engine)