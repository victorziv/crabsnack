#!/usr/bin/env python

import os
import pytest
import argparse
from config import config
from app import create_app
from app.dbmodels.query_admin import DBAdmin
# __________________________________


def resetdb(dba, conf):

    dba.conn, dba.cursor = dba.connectdb(conf.DB_CONN_URI_ADMIN)
    dba.dropdb(conf.DBNAME)
    dba.createdb(conf.DBNAME, conf.DBUSER)
    dba.cursor.close()
    dba.conn.close()
# __________________________________


def insert_initial_data(conf):
    app = create_app(conf.APPTYPE)
    app_context = app.app_context()
    app_context.push()
    from app.models import Role
    Role.insert_roles()
    from app.models import User
    User.insert_initial_users()
# __________________________________


def migratedb(conf, version=None):
    dba = DBAdmin(conf=conf)
    resetdb(dba, conf)
    dba.conn, dba.cursor = dba.connectdb(conf.DB_CONN_URI)
    dba.create_table_changelog()
    dba.db_upgrade(version)

    insert_initial_data(conf)

    dba.cursor.close()
    dba.conn.close()
# __________________________________


def parseargs():
    d = "Trigger one or more unittests"
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument(
        '-k', '--configkey', dest='configkey', default='testing',
        help="""Application type: testing, development, production. Default: testing""")

    return parser.parse_args()
# __________________________________


def main():
    """
    Example for literal string interpolation (f-string)
    """
    opts = parseargs()
    print("Configuration key: {}".format(opts.configkey))
    conf = config[opts.configkey]
    migratedb(conf)
    pytest.main(['-x', '-v', os.path.join(conf.BASEDIR, 'app', 'tests', 'test_follow.py')])
# __________________________________


if __name__ == '__main__':
    main()
