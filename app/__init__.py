from flask import Flask

app = Flask(__name__)

# import routes AFTER app is created
from app import routes
