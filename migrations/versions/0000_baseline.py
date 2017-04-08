#!/usr/bin/env python
import datetime
from psycopg2.extras import DictCursor


def insert_initial_record(conn, version, name):
    print("Insert: ")
    print("version: {} ".format(version))
    print("name: {} ".format(name))

    try:
        query = """
            INSERT INTO changelog
                (version, name, applied)
            VALUES (%s, %s, %s)
            RETURNING id
        """

        params = (version, name, datetime.datetime.now())

        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            conn.commit()
            fetch = cursor.fetchone()
            print("New record ID: {}".format(fetch['id']))
            return fetch['id']

    except Exception as e:
        print('ERROR: %s' % e)
        conn.rollback()
        return
# ____________________________


def create_changelog(conn):
    query = """
        CREATE TABLE IF NOT EXISTS changelog (
            id serial PRIMARY KEY,
            version VARCHAR(4) UNIQUE,
            name VARCHAR(64) UNIQUE,
            applied TIMESTAMP,
            comment VARCHAR(255)
        );
    """
    params = ()

    with conn.cursor() as cursor:
        cursor.execute(query, params)

    conn.commit()
# _______________________________


def upgrade(conn, version, name):
    create_changelog(conn)
    insert_initial_record(conn, version, name)
# _______________________________


def downgrade(conn):
    pass
