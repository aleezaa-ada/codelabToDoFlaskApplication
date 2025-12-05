from flask import Blueprint, render_template, redirect, url_for, flash, session
from . import db
from .models import User, Todo
from .forms import DeleteForm, EditTaskForm, LoginForm, RegisterForm, TaskForm
from functools import wraps

main = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in first.", "error")
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return wrapper


@main.route('/')
def start():
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return redirect(url_for('main.register'))

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for('main.login'))

    return render_template("register.html", form=form)

@main.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User does not exist", "error")
            return render_template("login.html", form=form)
        
        if not user.check_password(password):
            flash("Incorrect password", "error")
            return render_template("login.html", form=form)

        # STORE user in the session
        session['username'] = username
        flash("You have been logged in.", "success")
        return redirect(url_for('main.home'))
    
    return render_template("login.html", form=form)

@main.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    flash("You have been logged out.", "success")
    return redirect(url_for('main.login'))


@main.route('/home')
@login_required
def home():
    name = session.get('username')
    if not name:
        return redirect(url_for('main.login'))
    return render_template('index.html', name=name)


#create
@main.route("/new-task/<name>", methods=['GET', 'POST'])
@login_required
def create_task(name):
    user = User.query.filter_by(username=name).first_or_404()
    form = TaskForm()

    if form.validate_on_submit():
        new_task = Todo(
            title=form.title.data,
            completed=False,
            owner=user
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('main.tasks', name=name))

    return render_template("new_task.html", name=name, form=form)

    
#read
@main.route("/tasks/<name>")
@login_required
def tasks(name):
    user = User.query.filter_by(username=name).first_or_404()
    todos = user.todos

    delete_form = DeleteForm() 

    return render_template("tasks.html", name=name, todos=todos, delete_form=delete_form)


#update
@login_required
@main.route("/edit-task/<name>/<int:task_id>", methods=['GET', 'POST'])
def edit_task(name, task_id):
    todo = Todo.query.get_or_404(task_id)
    form = EditTaskForm(obj=todo)

    if form.validate_on_submit():
        todo.title = form.title.data
        todo.completed = form.completed.data
        db.session.commit()
        flash("Task updated!", "success")
        return redirect(url_for('main.tasks', name=name))

    return render_template("edit_task.html", form=form, todo=todo, name=name)

#delete
@main.route("/delete-task/<name>/<int:task_id>", methods=['POST'])
@login_required
def delete_task(name, task_id):
    form = DeleteForm()
    if form.validate_on_submit():
        todo = Todo.query.get_or_404(task_id)
        db.session.delete(todo)
        db.session.commit()
        flash("Task deleted!", "success")
    return redirect(url_for('main.tasks', name=name))

