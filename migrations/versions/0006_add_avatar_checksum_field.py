#!/usr/bin/env python


def upgrade(conn, **kwargs):
    query = """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS avatar_hash VARCHAR(32)
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()


# _______________________________


def downgrade(conn, **kwargs):
    query = """
        ALTER TABLE users
        DROP COLUMN IF EXISTS avatar_hash
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
