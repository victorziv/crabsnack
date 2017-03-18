from __future__ import print_function
from flask_script import Manager
from crabsnack import create_app
app = create_app()
manager = Manager(app)


@manager.command
def hello():
    print("Welcome to the wonderful world of Flask-Script")


if __name__ == '__main__':
    manager.run()
