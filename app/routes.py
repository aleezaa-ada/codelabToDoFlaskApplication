from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db
from .models import User, Todo
from .forms import LoginForm, RegisterForm, TaskForm

main = Blueprint('main', __name__)


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

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # 🔍 DEBUG — shows why validation is failing
    print("VALID:", form.validate_on_submit())
    print("errors:", form.errors)

    if form.validate_on_submit():  # POST + valid
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User does not exist", "error")
            return render_template("login.html", form=form)
        
        if not user.check_password(password):
            flash("Incorrect password", "error")
            return render_template("login.html", form=form)

        return redirect(url_for('main.home', name=username))

    return render_template("login.html", form=form)

@main.route('/home')
def home():
    name = request.args.get('name')
    return render_template('index.html', name=name)


#create
@main.route("/new-task/<name>", methods=['GET', 'POST'])
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
def tasks(name):
    user = User.query.filter_by(username=name).first_or_404()
    todos = user.todos
    return render_template("tasks.html", name=name, todos=todos)

@main.route("/task/<name>/<int:task_id>")
def task(name, task_id):
    todo = Todo.query.get_or_404(task_id)
    return f"<h1>Task detail page for task {todo.title}</h1>"

#update
@main.route("/edit-task/<name>/<int:task_id>", methods=['GET', 'POST'])
def edit_task(name, task_id):
    todo = Todo.query.get_or_404(task_id)
    if request.method == 'POST':
        todo.title = request.form.get('title')
        todo.completed = 'completed' in request.form
        db.session.commit()
        flash("Task updated!", "success")
        return redirect(url_for('main.tasks', name=name))
    return render_template("edit_task.html", todo=todo, name=name)

#delete
@main.route("/delete-task/<name>/<int:task_id>", methods=['POST'])
def delete_task(name, task_id):
    todo = Todo.query.get_or_404(task_id)
    db.session.delete(todo)
    db.session.commit()
    flash("Task deleted!", "success")
    return redirect(url_for('main.tasks', name=name))

@main.route('/logout')
def logout():
    return redirect(url_for('main.login'))
