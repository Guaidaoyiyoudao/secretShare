from app.models import User,Secret,SubSecret
from app.models import db


def create_table():
    db.connect()
    db.create_tables([User,Secret,SubSecret])
    db.close()
    
if __name__ == "__main__":
    create_table()