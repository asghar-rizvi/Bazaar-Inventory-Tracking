from flask import Flask, request, jsonify
from model import db, Product, StockMovement

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)

@app.route('/product', methods = ['POST'])
def add_product():
    data = request.get_json()
    product = Product(
        name = data['name'],
        description = data.get('description')
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'id':product.id}), 201

@app.route('/products/<int:product_id>/stock', methods = ['POST'])
def record_movement(product_id):
    data = request.get_json()
    movement = StockMovement(
        product_id = product_id,
        quantity = data['quantity'],
        movement_Type = data['movement_type'],
        notes = data.get('notes')
    )
    db.session.add(movement)
    db.session.commit()
    
    return jsonify({'id' : movement.id}), 201

@app.route('/inventory/products/<int:product_id>', methods= ['GET'])
def view_inventory(product_id):
    movement = StockMovement.query.filter_by(product_id = product_id).all()
    current_quantity = sum(m.quantity if m.movement_Type == 'stock_in' else -m.quantity 
                          for m in movement)  # Substracting the sales, removal and returning the currently in stock
    
    return jsonify({'product id' : product_id, 'Quantity' : current_quantity})


if __name__ == '__main__' :
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)

    
    