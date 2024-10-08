from flask import Flask
from flask.cli import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "main.login"  # Adjusted for blueprint
login_manager.login_message_category = "info"
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # Setup logging
    if not app.debug and not app.testing:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler("logs/ecommerce_app.log", maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("E-commerce App startup")

    with app.app_context():
        from . import models

        # Import Blueprints
        from .routes import main_bp
        from .admin_routes import admin_bp

        # Register Blueprints
        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp)

        db.create_all()

        # Apply migrations
        try:
            upgrade()
            app.logger.info("Database migrations applied successfully.")
        except Exception as e:
            app.logger.error(f"Error applying migrations: {e}")

        # Create admin user if environment variables are set and no admin exists
        admin_email = os.environ.get("ADMIN_EMAIL")
        admin_password = os.environ.get("ADMIN_PASSWORD")
        if admin_email and admin_password:
            admin_user = models.User.query.filter_by(email=admin_email).first()
            if not admin_user:
                admin_user = models.User(username="admin", email=admin_email)
                admin_user.set_password(admin_password)
                admin_user.is_admin = True
                db.session.add(admin_user)
                db.session.commit()
                app.logger.info("Admin user created.")

    return app
