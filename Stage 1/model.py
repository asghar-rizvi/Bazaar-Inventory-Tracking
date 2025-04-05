from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default = db.func.current_timestamp())
    
class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable= False)
    quantity = db.Column(db.Integer, nullable = False)
    movement_Type = db.Column(db.String(20), nullable = False)
    notes = db.Column(db.String(255), nullable =False)
    created_at = db.Column(db.DateTime(), default = db.func.current_timestamp())
    
    product = db.relationship('Product', backref = 'movements')