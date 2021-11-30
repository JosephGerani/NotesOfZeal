from website import myobj, db
from website.models import User, ToDoList, FlashCards
from flask import render_template, flash, redirect, url_for, request
from website.forms import LoginForm, SignupForm, ToDoListForm, CreateFlashCardForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

@myobj.route("/")
@login_required
def mainMenu():
    return redirect(url_for('login'))
    
@myobj.route("/home")
@login_required
def home():
    return render_template('home.html')

@myobj.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = False)
                return redirect(url_for('home'))

        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form = form)


@myobj.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@myobj.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()


    if form.validate_on_submit():
        hashedpassword = generate_password_hash(form.password.data, method = 'sha256')
        newUser = User(username = form.username.data, email = form.email.data, password = hashedpassword)
        db.session.add(newUser)
        db.session.commit()

        return '<h1>New user has been created</h1>'

    return render_template('signup.html', form = form)

@myobj.route('/todolist', methods = ['GET', 'POST'])
def todotlist():
    form = ToDoListForm()
    if request.method == 'POST':
        content = request.form['name']
        newtask = ToDoList(name = content)
        try:
            db.session.add(newtask)
            db.session.commit()
            return redirect('/todolist')
        except:
            return flash('Error')
    else:
        tasks = ToDoList.query.all()
        return render_template('todolist.html', tasks = tasks, form = form)

@myobj.route('/delete/<int:id>')
def delete(id):
    delete_task = ToDoList.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect ('/todolist')
    except:
        return flash ('Error')

@myobj.route('/createflashcards', methods = ['GET', 'POST'])
def createflash():
    form = CreateFlashCardForm()
    if form.validate_on_submit():
        newfc = FlashCards(fcname = form.fcname.data, fcdescription = form.fcdescription.data)
        try:
            db.session.add(newfc)
            db.session.commit()
            return redirect('/createflashcards')
        except:
            return flash ('error')
    else:
        flashcards = FlashCards.query.all()
        return render_template('createflashcard.html', form=form, flashcards=flashcards)

@myobj.route('/deleteflashcards/<int:id>', methods = ['GET', 'POST'])
def deleteflash(id):
    delete_flash = FlashCards.query.get_or_404(id)
    try:
        db.session.delete(delete_flash)
        db.session.commit()
        return redirect ('/viewflashcards')
    except:
        return flash('Error')

@myobj.route('/viewflashcards')
def viewflash():
    flashcards = FlashCards.query.all()
    return render_template('viewflashcards.html', flashcards=flashcards)
