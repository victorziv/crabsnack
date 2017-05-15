#!/usr/bin/env python


def add_column_authorid(conn):
    query = """
        ALTER TABLE posts
        ADD COLUMN IF NOT EXISTS authorid INT,
        ADD FOREIGN KEY (authorid) REFERENCES users (id) ON DELETE CASCADE
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()

# _______________________________


def drop_column_authorid(conn, **kwargs):
    query = """
        ALTER TABLE posts
        DROP CONSTRAINT IF EXISTS authorid_fk CASCADE
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def upgrade(conn, **kwargs):
    add_column_authorid(conn)
# _______________________________


def downgrade(conn, **kwargs):
    drop_column_authorid(conn)
