from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os


db = SQLAlchemy()
cache = Cache()
auth = HTTPBasicAuth()
socketio = SocketIO()

def create_app(register_blueprints=True):
    app = Flask(__name__)
    
    # Default Configuration
    app.config.update({
        # MASTER (write) - port 5432
        'SQLALCHEMY_DATABASE_URI': os.getenv('DB_URI', 'postgresql://postgres:asghar@localhost:5434/bazaar_stage3'),
        
        # REPLICA (read) - port 5433
        'SQLALCHEMY_BINDS': {
            'replica': os.getenv('REPLICA_URI', 'postgresql://postgres:asghar@localhost:5435/bazaar_stage3')
        },
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': os.getenv('REDIS_URI', 'redis://localhost:6379/0'),
        'SECRET_KEY': os.getenv('SECRET_KEY', 'dev-key-123'),
        'CELERY_BROKER_URL': os.getenv('CELERY_BROKER', 'redis://localhost:6379/0'),
        'CELERY_RESULT_BACKEND': os.getenv('CELERY_BACKEND', 'redis://localhost:6379/0')
    })

    # if config:
    #     app.config.update(config)
    
    # Initialize extensions with app
    db.init_app(app)
    cache.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Set up rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_limiter_key,
        storage_uri="redis://localhost:6379/1",
        default_limits=["200/day", "50/hour"]
    )
    
    # Register blueprints
    if register_blueprints:
        from routes import api_bp
        app.register_blueprint(api_bp)
    return app

# Helper function for rate limiting
def get_limiter_key():
    from flask import request
    if auth.current_user():
        return f"{get_remote_address()}_{auth.current_user()}"
    return f"{get_remote_address()}_anon"