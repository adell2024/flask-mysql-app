import time

from flask import Flask
from app.database import db


def create_app(config=None):
    """Application factory for Flask app initialization.
    
    Args:
        config (dict): Optional config dict to override default settings
    """
    app = Flask(__name__)
    
    # Default configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://app_user:app_password@db:3306/app_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Override with custom config if provided
    if config:
        app.config.update(config)
    
    db.init_app(app)
    
    with app.app_context():
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
    app.register_blueprint(api_bp)
    
    return app
