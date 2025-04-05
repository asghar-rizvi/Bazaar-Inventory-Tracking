from app import app, db
from model import Store, ProductCatalog, StoreInventory, User

def initialize_database():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

def add_user_table():
    with app.app_context():
        User.__table__.create(db.engine)

if __name__ == '__main__':
    # initialize_database()
    add_user_table()