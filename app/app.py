from flask import Flask

app = Flask(__name__)

# Import routes AFTER app is created
import routes

if __name__ == '__main__':
    app.run(debug=True)
