# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from decouple import config

from app import db, login_manager

from app.base.util import hash_pass

SECRET_KEY = config('SECRET_KEY')

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(Binary)

    def __repr__(self):
        return str(self.username)

    def get_reset_token(self, expires_sec=180):
        s = Serializer(SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')    

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)    

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
