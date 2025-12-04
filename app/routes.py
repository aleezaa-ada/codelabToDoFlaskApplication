from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Todo, User

main = Blueprint('main', __name__)


@main.route('/')
def start():
    return render_template('login.html')


@main.route('/login', methods=['POST', 'GET'])
def login():
    user_name = request.form['nm']
    user = User.query.filter_by(username=user_name).first()

    if not user:
        user = User(username=user_name, password_hash="")  # no password for now
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('main.home', name=user.username))

@main.route('/home')
def home():
    name = request.args.get('name')
    return render_template('index.html', name=name)


#create
@main.route("/new-task/<name>", methods=['GET', 'POST'])
def create_task(name):
    user = User.query.filter_by(username=name).first_or_404()
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            new_task = Todo(title=title, completed=False, owner=user)
            db.session.add(new_task)
            db.session.commit()
            flash("Task created!", "success")
            return redirect(url_for('main.tasks', name=name))
        else:
            flash("Title cannot be empty", "error")
            
    return render_template("new_task.html", name=name)
    
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
