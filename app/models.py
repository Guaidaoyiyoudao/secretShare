from peewee import *

db = SqliteDatabase('secret.db')

class Base(Model):

    class Meta:
        database = db

class User(Base):

    id = IntegerField(primary_key=True,index=True)
    username = CharField(unique=True)
    password = CharField()

    @classmethod
    def generate_password_hash(self,password):
        pass


class SubSecret(Base):

    id = IntegerField(primary_key=True,index=True)
    userId = ForeignKeyField(User,User.id,'subSecret')


class Secret(Base):
    userId = ForeignKeyField(User,User.id,'secret')
    subSecId = ForeignKeyField(SubSecret,SubSecret.id)
    id = AutoField(primary_key=True)
    secImg = CharField()
