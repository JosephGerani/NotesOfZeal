from flask import render_template, url_for, flash, redirect, request
from app import myapp_obj, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


# different URL the app will implement
@myapp_obj.route("/")
@myapp_obj.route("/home")
# called view function
def hello():
    return render_template('hello.html')

@myapp_obj.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('hello'))
    return render_template('register.html', title='Register', form=form)

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('hello'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@myapp_obj.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@myapp_obj.route("/req")
# user needs to be logged in to see this page
# needs to be user route!
@login_required
# called view function
def req():
    return '''<html><body>
    User needs to be logged in
    </body>
    </html>'''
