from celery import Celery
from datetime import datetime
import os

REDIS_URI = os.environ.get('REDIS_URI', 'redis://redis:6379/0')
CELERY_BROKER = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND', 'redis://redis:6379/0')



def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

# Create a standalone celery instance
celery = Celery(
    'inventory_app',
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND
)

celery.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
@celery.task(bind=True, max_retries=3)
def async_stock_update(self, store_id, product_id, quantity_change, user_id="system"):
    """Background stock update with audit logging"""
    try:
        from app_factory import db, socketio
        from model import StoreInventory
        
        # Create a Flask app context for this task
        from flask import Flask
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'postgresql://postgres:asghar@localhost/Bazaar_Stage3')
        db.init_app(app)
        
        with app.app_context():        
            item = StoreInventory.query.filter_by(
                store_id=store_id,
                product_id=product_id
            ).first()
            
            if not item:
                # Create new inventory item if it doesn't exist
                item = StoreInventory(
                    store_id=store_id,
                    product_id=product_id,
                    quantity=0
                )
                db.session.add(item)
            
            old_quantity = item.quantity
            item.quantity += quantity_change
            item.last_updated = datetime.utcnow()
            db.session.commit()
            
            # Log audit
            log_audit.delay(
                user_id=user_id,
                action="stock_update",
                record_type="inventory",
                record_id=item.id,
                old_value={"quantity": old_quantity},
                new_value={"quantity": item.quantity},
                ip_address=None
            )
            
            # Real-time update via websocket
            update_data = {
                'product_id': product_id,
                'quantity': item.quantity,
                'store_id': store_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Send websocket notification (outside app context, will be picked up by main app)
            socketio.emit('stock_update', update_data, room=f"stock_{store_id}_{product_id}")
            
            return True
    except Exception as e:
        self.retry(exc=e, countdown=60)

@celery.task
def log_audit(user_id, action, record_type, record_id, old_value, new_value, ip_address=None):
    """Async audit logging"""
    # Import here to avoid circular imports
    from app_factory import db
    from model import AuditLog
    
    # Create a Flask app context for this task
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'postgresql://postgres:asghar@localhost/Bazaar_Stage3')
    db.init_app(app)
    
    with app.app_context():
        log = AuditLog(
            user_id=user_id,
            action=action,
            record_type=record_type,
            record_id=record_id,
            old_values=old_value,
            new_values=new_value,
            ip_address=ip_address
        )
        db.session.add(log)
        db.session.commit()