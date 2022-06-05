from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, IngestForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

#Main Page
@app.route('/')
def splash():
    return render_template('splash.html', title='Welcome to beanZ')

@app.route('/index', methods=['GET', 'POST'])
@login_required #when a user that is not logged in attempts access, will be redirected to login page.
def index():
    user = {'username': 'Eric'}
    
    form = IngestForm()
    if form.validate_on_submit():
        flash('Ingest the files!')

    return render_template('index.html', title='beanZ Home', form=form)

#Login Page
@app.route('/login', methods=['GET', 'POST']) #POSTs are for browser submitting form data to the server
def login():
    #if current user is already logged in, go to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#Logs the user out and redirects back to index
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Register a new user
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#User profile page
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    #can pass additional things into render_templater here
    transactions = [
        {'owner': user, 'body': 'Transaction1 data'},
        {'owner': user, 'body': 'Transaction2 data'}]
    return render_template('user.html', user=user, transcations=transactions)

#Adding last seen functionality
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()