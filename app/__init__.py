from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.podcasts import podcasts_bp
    from app.routes.brands import brands_bp
    from app.routes.campaigns import campaigns_bp
    from app.routes.deals import deals_bp
    from app.routes.analytics import analytics_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(podcasts_bp)
    app.register_blueprint(brands_bp)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(deals_bp)
    app.register_blueprint(analytics_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
