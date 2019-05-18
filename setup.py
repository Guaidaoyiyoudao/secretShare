from app.models import User,Secret,SubSecret,ResetPassword
from app.models import db


def create_table():
    db.connect()
    db.create_tables([User,Secret,SubSecret,ResetPassword])
    db.close()
    
if __name__ == "__main__":
    create_table()