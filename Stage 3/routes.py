# routes.py
from flask import Blueprint, request, jsonify, current_app, g
from flask_socketio import join_room
from app_factory import db, cache, auth, socketio
from model import User, AuditLog, StoreInventory
from async_task import async_stock_update
from functools import wraps
import json

api_bp = Blueprint('api', __name__)

# Auth setup
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        g.current_user = user
        return username
    return None

# Helper for input validation
def validate_json(*required_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({"error": "Missing JSON data"}), 400
            
            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return jsonify({
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                }), 400
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# WebSocket handlers
@socketio.on('connect')
def handle_connect():
    socketio.emit('ack', {'status': 'connected'})

@socketio.on('subscribe_stock')
def handle_subscribe(data):
    if 'store_id' in data and 'product_id' in data:
        join_room(f"stock_{data['store_id']}_{data['product_id']}")
        socketio.emit('subscribed', {
            'store_id': data['store_id'],
            'product_id': data['product_id']
        })
    else:
        socketio.emit('error', {'message': 'Missing store_id or product_id'})

# API Endpoints
@api_bp.route('/stock', methods=['POST'])
@auth.login_required
@validate_json('store_id', 'product_id', 'quantity')
def update_stock():
    """Async stock update endpoint"""
    data = request.get_json()
    
    # Get current user for audit trail
    user_id = g.current_user.username if hasattr(g, 'current_user') else "system"
    
    # Validate input data
    try:
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        quantity_change = int(data['quantity'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data types"}), 400
    
    # Queue the async task
    task = async_stock_update.delay(
        store_id=store_id,
        product_id=product_id,
        quantity_change=quantity_change,
        user_id=user_id
    )
    
    return jsonify({
        "status": "queued",
        "message": "Update processing started",
        "task_id": task.id
    }), 202
    
    
@api_bp.route('/stock/<int:store_id>', methods=['GET'])
@cache.cached(timeout=30, query_string=True)
@auth.login_required
def get_stock(store_id):
    """Cached read endpoint using replica database"""
    try:
        # Use the read replica for this query
        replica_engine = db.get_engine(current_app, bind='replica')
        
        # Create a session using the provided engine
        Session = db.sessionmaker(bind=replica_engine)
        
        with Session() as session:
            stock = session.query(StoreInventory).filter_by(store_id=store_id).all()
            
            result = [{
                "product_id": item.product_id,
                "quantity": item.quantity,
                "last_updated": item.last_updated.isoformat()
            } for item in stock]
            
            return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error fetching stock: {e}")
        return jsonify({"error": "Failed to fetch inventory data"}), 500

@api_bp.route('/audit/logs', methods=['GET'])
@auth.login_required
def get_audit_logs():
    """Fetch audit logs"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 100, type=int), 100)  # Limit to 100 logs per page
        
        logs = AuditLog.query.order_by(
            AuditLog.created_at.desc()
        ).paginate(page=page, per_page=per_page)
        
        return jsonify({
            "total": logs.total,
            "pages": logs.pages,
            "current_page": page,
            "logs": [{
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "record_type": log.record_type,
                "record_id": log.record_id,
                "timestamp": log.created_at.isoformat(),
                "old_values": log.old_values,
                "new_values": log.new_values
            } for log in logs.items]
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching audit logs: {e}")
        return jsonify({"error": "Failed to fetch audit logs"}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "ok",
        "version": "1.0.0"
    })