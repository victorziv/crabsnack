import sys
import os
from app.dbmodels.query_admin import DBAdmin
from config import config
from app import create_app, dba
from app import models
from flask_script import Manager, Shell

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
# ___________________________________________


def make_shell_context():
    context = {}
    context.update(dict(app=app, dba=dba, models=models))
    return context
# ___________________________________________


manager.add_command("shell", Shell(
    make_context=make_shell_context, use_ipython=True))
# ___________________________________________


@manager.option(
    '-v', '--version', dest='version', default=None,
    help="""
    Version: if provided upgrade/downgrade up/down to the version.
    Default: None, up to the last version, down - to the previous version.
    """
)
@manager.option(
    'action',
    choices=['upgrade', 'downgrade', 'reset'],
    help="""
        Actions:
            upgrade - upgrade DB up to provided version or the last available.
            downgrade - downgrade down to the provided version or to the previous one.
    """
)
@manager.option(
    'configkey',
    choices=['testing', 'development', 'production'],
    help="Configuration key: testing, develop or production"
)
def db(configkey, action, version=None):
    """
    Upgrades / downgrades DB up / down to some version.
    """
    conf = config[configkey]
    dba = DBAdmin(conf=conf)

    try:
        dba.conn, dba.cursor = dba.connectdb(dba.conf.DB_CONN_URI)
        if action == 'upgrade':
            dba.db_upgrade(version)
        elif action == 'downgrade':
            dba.db_downgrade(version)
        elif action == 'reset':
            reset_db(configkey)
        else:
            print("ERROR: unsupported action {}".format(action))
            sys.exit(1)

    finally:
        dba.conn.close()
# ___________________________________________


def prepare_db(configkey):
    reset_db(configkey)
    db(configkey, 'upgrade')
#     dbmigrate(configkey, 'upgrade')
# ___________________________________________


def reset_db(configkey):
    dbadmin = DBAdmin(conf=config[configkey])
    dbadmin.dropdb()
    dbadmin.cretedb()
# ___________________________________________


@manager.command
def test(coverage=False):
    """Run the unittests"""

    prepare_db('testing')

    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import pytest
    pytest.main(['-v', 'app/tests/'])

    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

# _____________________________


if __name__ == '__main__':
    manager.run()
