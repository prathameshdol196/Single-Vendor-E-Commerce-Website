from flask import Flask
from flask.cli import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Adjusted for blueprint
login_manager.login_message_category = 'info'
bootstrap = Bootstrap()

def create_app():

    load_dotenv()  # Load environment variables from .env
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        from . import models

        # Import Blueprints
        from .routes import main_bp
        from .admin_routes import admin_bp

        # Register Blueprints
        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp)

        db.create_all()

    return app
