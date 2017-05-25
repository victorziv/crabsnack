import sys
import os
from app.dbmodels.query_admin import DBAdmin
from config import config
from app import create_app, db
from app import models
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
# ___________________________________________


def make_shell_context():
    context = {}
    context.update(dict(app=app, db=db, models=models))
    return context
# ___________________________________________


manager.add_command("shell", Shell(
    make_context=make_shell_context, use_ipython=True))
manager.add_command("db", MigrateCommand)
# ___________________________________________


def prompt(question):
    from distutils.util import strtobool

    sys.stdout.write('{} [y/n]: '.format(question))
    val = input()
    try:
        ret = strtobool(val)
    except ValueError:
        sys.stdout.write('Please answer with a y/n\n')
        return prompt(question)

    return ret
# ___________________________________________


def dbdrop(dba, conf, conn):
    sure = prompt("You are about to drop {} DB. Sure?".format(conf.DBNAME))
    if not sure:
        sys.exit(1)

    dba.dropdb(conn, conf.DBNAME)
# ___________________________________________


# def createdb(dba, conf, conn_admin):
#     print("===> CREATE DBNAME: {}".format(conf.DBNAME))
#     dba.createdb(conn_admin, conf.DBNAME, conf.DBUSER)
#     conn = dba.connectdb(conf.DB_CONN_URI)
#     dba.create_baseline(conn)
# ___________________________________________


@manager.option(
    'action',
    choices=['drop', 'create', 'reset'],
    help="""
        Actions:
            drop - remove the DB for <configkey>
            create - create a new DB for <cofigkey>
            reset - re-create ( drop & create ) the DB
    """
)
@manager.option(
    'configkey',
    choices=['testing', 'development', 'production'],
    help="Configuration key: testing, develop or production"
)
def dbinit(configkey, action):
    """
    Creates, drops or re-creates(reset) a DB.
    """
    conf = config[configkey]
    dba = DBAdmin(conf=conf)
    conn = dba.connectdb(conf.DB_CONN_URI_ADMIN)

    try:
        if action == 'drop':
            dba.dbdrop()
        elif action == 'create':
            dba.createdb()
        elif action == 'reset':
            dba.dbdrop()
            dba.createdb(dba, conf, conn)
        else:
            print("ERROR: unsupported action {}".format(action))
            sys.exit(1)

    finally:
        conn.close()
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
    choices=['upgrade', 'downgrade'],
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
def dbmigrate(configkey, action, version=None):
    """
    Upgrades / downgrades DB up / down to some version.
    """
    conf = config[configkey]
    dba = DBAdmin(conf=conf)

    try:
        dba.conn, dba.cur = dba.connectdb(dba.conf.DB_CONN_URI)
        if action == 'upgrade':
            dba.db_upgrade(version)
        elif action == 'downgrade':
            dba.db_downgrade(version)
        else:
            print("ERROR: unsupported action {}".format(action))
            sys.exit(1)

    finally:
        dba.conn.close()
# ___________________________________________


def prepare_db(configkey):
    reset_db(configkey)
    dbmigrate(configkey, 'upgrade')
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
