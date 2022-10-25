from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email

'''
#Main Page
@app.route('/')
def splash():
    #if current user is already logged in, go to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    return render_template('splash.html', title='Welcome to beanZ')

#Features Page
@app.route('/features')
def features():
    return render_template('features.html', title='beanZ Features')

#Pricing Page
@app.route('/pricing')
def pricing():
    return render_template('pricing.html', title='beanZ Pricing')

#contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html', title='beanZ Contact')

#Index Page
@app.route('/index', methods=['GET', 'POST'])
@login_required #when a user that is not logged in attempts access, will be redirected to login page.
def index():
    user = {'username': 'Eric'}
    
    form = IngestForm()
    if form.validate_on_submit():
        flash('Ingest the files!')

    return render_template('index.html', title='beanZ Home', form=form)
'''

#Login Page
@bp.route('/login', methods=['GET', 'POST']) #POSTs are for browser submitting form data to the server
def login():
    #if current user is already logged in, go to index
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

#Logs the user out and redirects back to index
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

#Register a new user
@bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

'''
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
'''

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('auth.login'))
        else:
            flash('No record of that email')
        
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)