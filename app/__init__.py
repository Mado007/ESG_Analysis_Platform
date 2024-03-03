from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_pyfile('instance/config.py')

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from app import routes
