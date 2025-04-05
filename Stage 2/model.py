from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Store(db.Model):
    __tablename__ = 'store' 
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(255), nullable=False)

class ProductCatalog(db.Model):
    __tablename__ = 'product_catalog'  
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))

class StoreInventory(db.Model):
    __tablename__ = 'store_inventory'  
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product_catalog.id'), nullable=False) 
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)  
    quantity = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    store = db.relationship('Store', backref='inventories')
    product = db.relationship('ProductCatalog', backref='inventories')