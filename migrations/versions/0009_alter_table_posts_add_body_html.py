#!/usr/bin/env python


def add_column_body_html(conn):
    query = """
        ALTER TABLE posts
        ADD COLUMN IF NOT EXISTS body_html TEXT
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()

# _______________________________


def drop_column_body_html(conn, **kwargs):
    query = """
        ALTER TABLE posts
        DROP COLUMN IF EXISTS body_html
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def upgrade(conn, **kwargs):
    add_column_body_html(conn)
# _______________________________


def downgrade(conn, **kwargs):
    drop_column_body_html(conn)
