from flask import Flask
from app.database import db


def create_app():
    """Application factory for Flask app initialization."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://app_user:app_password@db:3306/app_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    # Import and register blueprints
    from app.main import api_bp
    app.register_blueprint(api_bp)
    
    return app
