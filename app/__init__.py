# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_path = os.path.join(os.getcwd(), 'instance', 'config.py')
if os.path.exists(config_path):
    app.config.from_pyfile(config_path)
else:
    raise FileNotFoundError("Config file not found")

# Set the secret key from configuration
app.secret_key = app.config['SECRET_KEY']

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
migrate = Migrate(app, db)

# Import routes and models
from app import routes, models
