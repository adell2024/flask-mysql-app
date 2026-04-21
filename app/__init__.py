import time

from flask import Flask
from app.database import db


def create_app(config=None):
    """Application factory for Flask app initialization.
    
    Args:
        config (dict): Optional config dict to override default settings
    """
    flask_app = Flask(__name__)
    
    # Default configuration
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://app_user:app_password@db:3306/app_db'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Override with custom config if provided
    if config:
        flask_app.config.update(config)
    
    db.init_app(flask_app)
    
    # Ensure model metadata is registered before creating tables.
    from app import models  # noqa: F401
    
    with flask_app.app_context():
        # Retry database initialization until MySQL is ready.
        for attempt in range(10):
            try:
                db.create_all()
                break
            except Exception:
                if attempt == 9:
                    raise
                time.sleep(2)
        
    # Import and register blueprints
    from app.main import api_bp
    flask_app.register_blueprint(api_bp)
    
    return flask_app
