from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('login.html')


@main.route("/tasks/<name>")
def tasks(name):
    return render_template("tasks.html", name=name)


@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
    else:
        user = request.args.get('nm')

    return redirect(url_for('main.tasks', name=user))


@main.route("/task/<name>/<int:task_id>")
def task(name, task_id):
    return f"<h1>Task detail page for task {task_id}</h1>"


@main.route("/new-task/<name>")
def create_task(name):
    return render_template("new_task.html", name=name)
