#!/usr/bin/env python


def create_table_posts(conn):
    query = """
        CREATE TABLE IF NOT EXISTS posts (
            id serial PRIMARY KEY,
            body TEXT,
            postdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    create_table_posts()
    create_index_postdate()

# _______________________________


def downgrade(conn, **kwargs):
    drop_post_index()
    drop_posts_table()
# _______________________________


def drop_post_index(conn):
    query = """
        DROP INDEX IF EXISTS postdate_index
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def drop_posts_table(conn):

    query = """
        DROP TABLE IF EXISTS posts
    """

    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
