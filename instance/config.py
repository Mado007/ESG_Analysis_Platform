import os

# Generate a secret key
SECRET_KEY = os.urandom(24)

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
