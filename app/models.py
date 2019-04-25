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

    
    def check_password(self,password_hash,pwd):
        return check_password_hash(password_hash,pwd)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.select().where(User.id==user_id).get()
    except DoesNotExist as e:
        return None

class SubSecret(Base):

    id = IntegerField(primary_key=True,index=True)
    user = ForeignKeyField(User,backref="subSecrets")
    secretHash = CharField(unique=True)
    subSecretHash = CharField(unique=True)


class Secret(Base):

    owner = ForeignKeyField(User,backref="secrets")
    secretHash = CharField(unique=True)
    id = AutoField(primary_key=True)
    shareNums = IntegerField() #分享给了多少个人
    hasNums = IntegerField() #
