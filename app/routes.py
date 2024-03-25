# Import necessary modules
from flask import render_template, flash, redirect, url_for
from flask_login import login_user
from flask import Blueprint
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm
import pandas as pd
import plotly.express as px
from app.dashboard import generate_plotly_figure, esg_data_df
from plotly.offline import plot
import os


bp = Blueprint('main', __name__)
# Ensure generate_plotly_figure is correctly defined in dashboard.py
# If it relies on specific data which may not be available, ensure to have checks or try-except blocks

# Index route
@bp.route('/')
@bp.route('/index')
def index():
    # Create sample data for demonstration
    df = pd.DataFrame({
        'Country': ['USA', 'Canada', 'UK', 'Germany', 'France'],
        'ESG_Score': [80, 75, 70, 85, 78],
        'Environmental': [85, 80, 75, 90, 82],
        'Social': [78, 76, 72, 80, 75],
        'Governance': [82, 79, 76, 88, 80]
    })

    # Create a bar chart using Plotly
    fig = px.bar(df, x='Country', y='ESG_Score', title='ESG Scores by Country')

    # Convert the Plotly figure to HTML format
    plot_html = fig.to_html(full_html=False, default_height=500)

    # Render the index.html template with the Plotly plot embedded
    return render_template('index.html', plot=plot_html)

# Dashboard route
@bp.route('/dashboard')
def dashboard():
    # Use previously defined functions for generating Plotly figures
    fig = generate_plotly_figure(esg_data_df)
    
    # Convert Plotly figure to HTML div
    fig_html = plot(fig, output_type='div', include_plotlyjs=True)
    
    # Render 'dashboard.html', passing the figure HTML
    return render_template('dashboard.html', fig_html=fig_html)

# Debug route for data paths
@bp.route('/data')
def debug_data_paths():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    file_paths = [
        os.path.join(data_dir, 'ESGData.csv'),
    ]

    file_existence = {path: os.path.exists(path) for path in file_paths}
    return str(file_existence)

# About route
# @bp.route('/about')
# def about():
#     return render_template('about.html', title='About')

# Register route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Instantiate the RegistrationForm
    if form.validate_on_submit():
        # Check if username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is not None:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('main.register'))

        # If username does not exist, proceed to create new user
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

# Login route
@bp.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('main.login'))
    
        # Log in the user using Flask-Login's login_user function
        login_user(user, remember=form.remember_me.data)
    
        # Redirect the user to the index page after successful login
        return redirect(url_for('main.index'))

    # Render the login form template
    return render_template('login.html', title='Sign In', form=form)

# Run the-app
# if __name__ == '__main__':
#     db.run(debug=True)
