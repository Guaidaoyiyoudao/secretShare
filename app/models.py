from peewee import *
from flask_login import UserMixin
from app import login_manager
from werkzeug.security import generate_password_hash,check_password_hash
db = SqliteDatabase('secret.db')

class Base(Model):

    class Meta:
        database = db

class User(UserMixin,Base):

    id = IntegerField(primary_key=True,index=True)
    username = CharField(unique=True)
    password_hash = CharField()

    
    @classmethod
    def check_password(self,pwd):
        return check_password_hash(self.password_hash,pwd)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    


@login_manager.user_loader
def load_user(user_id):
    return User.select().where(User.id==user_id).get()

class SubSecret(Base):

    id = IntegerField(primary_key=True,index=True)
    userId = ForeignKeyField(User,User.id,'subSecret')
    secImg = CharField(unique=True)

class Secret(Base):
    userId = ForeignKeyField(User,User.id,'secret')
    subSecId = ForeignKeyField(SubSecret,SubSecret.id)
    id = AutoField(primary_key=True)
    secImg = CharField()
