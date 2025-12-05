from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Register")

class TaskForm(FlaskForm):
    title = StringField("Task Title", validators=[DataRequired()])
    submit = SubmitField("Create Task")

class EditTaskForm(FlaskForm):
    title = StringField("Task Title", validators=[DataRequired()])
    completed = BooleanField("Completed")   
    submit = SubmitField("Save")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
