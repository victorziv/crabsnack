#!/usr/bin/env python


def upgrade(conn, version, name):
    try:
        query = """
            CREATE TABLE IF NOT EXISTS installationstep (
                id serial PRIMARY KEY,
                name VARCHAR(32) UNIQUE,
                display_name VARCHAR(64),
                priority INTEGER
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
            DROP TABLE IF EXISTS installationstep
        """
        params = ()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

    except Exception as e:
        print('ERROR: %s' % e)
        conn.rollback()
        return
