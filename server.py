from flask_app import app
from datetime import datetime
from flask_app.controllers import trips, users

if __name__ == '__main__':
    app.run(debug = True)