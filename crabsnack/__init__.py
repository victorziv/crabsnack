import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'ejkfhbwi242ri'
    app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))

    @app.route('/')
    def index():
        return "What's up!"

    return app
