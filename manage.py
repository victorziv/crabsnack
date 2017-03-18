from __future__ import print_function
from flask_script import Manager
from crabsnack import create_app
app = create_app()
manager = Manager(app)


@manager.command
def hello():
    """ Welcoming heartily. """
    print("Welcome to the wonderful world of Flask-Script")


@manager.option('-n', '--name', help="Enter your name, please")
def hi(name):
    print("Hi there, {}".format(name))


if __name__ == '__main__':
    manager.run()
