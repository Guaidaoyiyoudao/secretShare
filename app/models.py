from peewee import *
from flask_login import UserMixin
from app import login_manager
from secrets import token_hex
from werkzeug.security import generate_password_hash,check_password_hash

db = SqliteDatabase('secret.db')

class Base(Model):

    class Meta:
        database = db

class User(UserMixin,Base):

    id = IntegerField(primary_key=True,index=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    verify_token = CharField(unique=True,default=token_hex(32))
    email_verified = BooleanField(default=False)
    password_hash = CharField()

    
    def check_password(self,password_hash,pwd):
        return check_password_hash(password_hash,pwd)
    
        
    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
class ResetPassword(Base):

    id = AutoField(primary_key=True)
    user = ForeignKeyField(User)
    token = CharField(unique=True,default=token_hex(32))

class Secret(Base):

    owner = ForeignKeyField(User,backref="secrets")
    name = CharField(unique=True)
    secretHash = CharField(unique=True)
    id = AutoField(primary_key=True)
    shareNums = IntegerField() #分享给了多少个人
    hasNums = IntegerField(default=0) #
    needNums = IntegerField()
    width = IntegerField()
    height = IntegerField()


class SubSecret(Base):

    id = IntegerField(primary_key=True,index=True)
    user = ForeignKeyField(User,backref="subSecrets")
    secret = ForeignKeyField(Secret,backref="subSecrets")
    subSecretHash = CharField(unique=True)
    saved = BooleanField(default=False)
    img = CharField(unique=True,default='')
    


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.select().where(User.id==user_id).get()
    except DoesNotExist:
        return None