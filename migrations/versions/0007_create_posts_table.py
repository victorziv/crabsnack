#!/usr/bin/env python


def create_table_posts(conn):
    query = """
        CREATE TABLE IF NOT EXISTS posts (
            id serial PRIMARY KEY,
            body TEXT,
            postdate TIMESTAMP WITHOUT TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
        );
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def create_index_postdate(conn):
    query = """
        CREATE INDEX IF NOT EXISTS postdate_index
        ON posts (postdate);
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def upgrade(conn, **kwargs):
    create_table_posts(conn)
    create_index_postdate(conn)

# _______________________________


def downgrade(conn, **kwargs):
    drop_index_posts(conn)
    drop_table_posts(conn)
# _______________________________


def drop_index_posts(conn):
    query = """
        DROP INDEX IF EXISTS postdate_index
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def drop_table_posts(conn):

    query = """
        DROP TABLE IF EXISTS posts
    """

    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
