#!/usr/bin/env python


def upgrade(conn, version, name):
    try:
        query = """
            CREATE TABLE IF NOT EXISTS roles (
                id serial PRIMARY KEY,
                name VARCHAR(64) UNIQUE,
                isdefault BOOLEAN DEFAULT FALSE,
                permissions INTEGER
            );
        """
        params = ()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

    except Exception as e:
        print('ERROR: %s' % e)
        conn.rollback()
        return
# _______________________________


def downgrade(conn):
    try:
        query = """
            DROP TABLE IF EXISTS roles
        """
        params = ()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

    except Exception as e:
        print('ERROR: %s' % e)
        conn.rollback()
        return
