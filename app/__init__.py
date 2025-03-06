from flask import Flask
from .config import Config
from .database import db
from flask_cors import CORS
from .routes.goal_routes import bp as goal_routes
from .routes.asset_routes import bp as asset_routes
from .routes.liability_routes import bp as liability_routes
from .routes.mapping_routes import bp as mapping_routes

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(goal_routes)
    app.register_blueprint(asset_routes)
    app.register_blueprint(liability_routes)
    app.register_blueprint(mapping_routes)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 