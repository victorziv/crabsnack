import argparse
from app.dbmodels.query_admin import DBAdmin
# __________________________________


def resetdb(conf):
    dba = DBAdmin(conf=conf)
    conn = dba.connectdb(conf.DB_CONN_URI_ADMIN)

    try:
        dba.dbdrop()
        dba.createdb()
    finally:
        conn.close()
# __________________________________


def parse_args():
    d = "Trigger one or more unittests"
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument(
        '-t', '--type', dest='apptype', default='testing',
        help="""Application type: testing, development, production. Default: testing""")

    return parser.parse_args()
# __________________________________


def main():
    opts = parse_args()
    print(opts)
