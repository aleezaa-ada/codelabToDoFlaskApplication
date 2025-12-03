from flask import render_template, request, redirect, url_for
from app import app

@app.route('/')
def home():
    return render_template('login.html')

@app.route("/tasks/<name>")
def tasks(name):
    return render_template("tasks.html", name=name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('tasks', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('tasks', name=user))

@app.route("/task/<name>/<int:task_id>")
def task(name, task_id):
    return f"<h1>Task detail page for task {task_id}</h1>"

@app.route("/new-task/<name>")
def create_task(name):
    return render_template("new_task.html", name=name)
