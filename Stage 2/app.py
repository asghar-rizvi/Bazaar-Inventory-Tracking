from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from model import db, Store, ProductCatalog, StoreInventory, User
import time
import redis
from flask import g


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:asghar@localhost/Bazaar Stage2'
db.init_app(app)

auth = HTTPBasicAuth()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

THROTTLE_INTERVAL = 2 

@app.before_request
def redis_throttle():
    ip = request.remote_addr
    key = f"last_request:{ip}"
    
    last_request_time = r.get(key)
    current_time = time.time()

    if last_request_time:
        elapsed = current_time - float(last_request_time)
        if elapsed < THROTTLE_INTERVAL:
            delay = THROTTLE_INTERVAL - elapsed
            time.sleep(delay)  
    
    r.set(key, current_time, ex=60)  

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return username

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username exists"}), 400
        
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201


@app.route('/stores', methods=['GET'])
@auth.login_required
def get_stores():
    stores = Store.query.all()
    return jsonify([{"id": s.id, "name": s.name, "location": s.location} for s in stores])



@app.route('/reports', methods=['GET'])
@auth.login_required
def get_report():
    store_id = request.args.get('store_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = StoreInventory.query
    if store_id:
        query = query.filter_by(store_id=store_id)
    if start_date and end_date:
        query = query.filter(StoreInventory.last_updated.between(start_date, end_date))
    
    results = query.all()
    return jsonify([{
        "store_id": r.store_id,
        "product_id": r.product_id,
        "quantity": r.quantity,
        "last_updated": r.last_updated
    } for r in results])

if __name__ == '__main__':
    with app.app_context():
        if not User.query.first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            
    app.run(debug=True)