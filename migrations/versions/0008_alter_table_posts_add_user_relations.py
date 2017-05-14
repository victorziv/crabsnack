#!/usr/bin/env python


def alter_table_posts(conn, **kwargs):
    query = """
        ALTER TABLE posts
        ADD COLUMN IF NOT EXISTS authorid INTEGER;
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()

# _______________________________


def alter_table_users(conn, **kwargs):
    query = """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS posts INTEGER;
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def drop_column_posts(conn, **kwargs):
    query = """
        ALTER TABLE posts DROP COLUMN IF EXISTS authorid;
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def drop_column_users(conn, **kwargs):
    query = """
        ALTER TABLE users DROP COLUMN IF EXISTS posts;
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def upgrade(conn, **kwargs):
    alter_table_posts()
    alter_table_users()
# _______________________________


def downgrade(conn, **kwargs):
    drop_column_posts(conn)
    drop_column_users(conn)
