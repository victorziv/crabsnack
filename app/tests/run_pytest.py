#!/usr/bin/env python

import argparse
from config import config
from app.dbmodels.query_admin import DBAdmin
# __________________________________


def resetdb(dba, db_to_reset, dbowner):

    try:
        dba.dropdb(db_to_reset)
        dba.createdb(db_to_reset, dbowner)
        dba.create_table_changelog()
    finally:
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
    dba.conn, dba.cursor = dba.connectdb(conf.DB_CONN_URI_ADMIN)
    resetdb(dba, conf.DBNAME, conf.DBUSER)
# __________________________________


if __name__ == '__main__':
    main()
