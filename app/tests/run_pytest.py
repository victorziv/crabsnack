#!/usr/bin/env python

import argparse
from config import config
from app.dbmodels.query_admin import DBAdmin
# __________________________________


def resetdb(dba, conf):

    dba.conn, dba.cursor = dba.connectdb(conf.DB_CONN_URI_ADMIN)
    dba.dropdb(conf.DBNAME)
    dba.createdb(conf.DBNAME, conf.DBUSER)
    dba.cursor.close()
    dba.conn.close()
# __________________________________


def migratedb(dba, conf, version=None):
    resetdb(dba, conf)

    dba.conn, dba.cursor = dba.connectdb(conf.DB_CONN_URI)
    dba.create_table_changelog()
    dba.db_upgrade(version)
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
    print(f"Configuration key: {opts.configkey}")
    conf = config[opts.configkey]
    dba = DBAdmin(conf=conf)
    migratedb(dba, conf)
# __________________________________


if __name__ == '__main__':
    main()
