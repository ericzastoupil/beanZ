from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

#Main Page
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Eric'}
    return render_template('index.html', title='Home', user=user)

#Login Page
@app.route('/login', methods=['GET', 'POST']) #POSTs are for browser submitting form data to the server
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/index')
    
    return render_template('login.html', title='Sign In', form=form)