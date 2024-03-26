import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Extensions instantiation
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Application factory function
def create_app(test_config=None):
    global db, login_manager, migrate
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder='static')
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',  # Overridden by instance config
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "app.sqlite")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    
    # Load configuration
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app import models, routes
    
    # Authentication
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import here to avoid circular import
        return User.query.get(int(user_id))
    
    # Blueprint registration and import routes
    from .routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    # Additional setup for routes, blueprints, commands etc.
    return app
