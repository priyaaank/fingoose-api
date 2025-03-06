from flask import Flask
from .config import Config
from .database import db
from flask_cors import CORS
from flask_migrate import Migrate
from .routes.goal_routes import bp as goal_routes
from .routes.asset_routes import bp as asset_routes
from .routes.liability_routes import bp as liability_routes
from .routes.mapping_routes import bp as mapping_routes

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS for development
    CORS(app, 
         origins=["http://localhost:3000", "http://127.0.0.1:3000"],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(goal_routes)
    app.register_blueprint(asset_routes)
    app.register_blueprint(liability_routes)
    app.register_blueprint(mapping_routes)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 