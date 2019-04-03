from peewee import *
from flask_login import UserMixin
from app import login_manager
db = SqliteDatabase('secret.db')

class Base(Model):

    class Meta:
        database = db

class User(UserMixin,Base):

    id = IntegerField(primary_key=True,index=True)
    username = CharField(unique=True)
    password = CharField()

    @classmethod
    def generate_password_hash(self,password):
        pass

@login_manager.user_loader
def load_user(user_id):
    return User.select().where(User.id==user_id)

class SubSecret(Base):

    id = IntegerField(primary_key=True,index=True)
    userId = ForeignKeyField(User,User.id,'subSecret')
    secImg = CharField(unique=True)

class Secret(Base):
    userId = ForeignKeyField(User,User.id,'secret')
    subSecId = ForeignKeyField(SubSecret,SubSecret.id)
    id = AutoField(primary_key=True)
    secImg = CharField()
