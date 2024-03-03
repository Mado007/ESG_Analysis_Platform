# Import necessary modules
from flask import render_template, flash, redirect, url_for
from flask_login import login_user
from app import app, db
from app.models import User
from app.forms import LoginForm 

 # Import the LoginForm class from the forms.py file

# Index route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# About route
@app.route('/about')
def about():
    return render_template('about.html', title='About')

# Register route
@app.route('/register')
def register():
    return render_template('register.html', title='Register')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Create an instance of the LoginForm
    form = LoginForm()
    
    # Handle form submission
    if form.validate_on_submit():
        # Query the User model to find the user by username
        user = User.query.filter_by(username=form.username.data).first()
        
        # Check if the user exists and the password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        # Log in the user using Flask-Login's login_user function
        login_user(user, remember=form.remember_me.data)
        
        # Redirect the user to the index page after successful login
        return redirect(url_for('index'))
    
    # Render the login form template
    return render_template('login.html', title='Sign In', form=form)
