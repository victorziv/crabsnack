#!/usr/bin/env python


def upgrade(conn, **kwargs):
    query = """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS location VARCHAR(64),
        ADD COLUMN IF NOT EXISTS about_me TEXT,
        ADD COLUMN IF NOT EXISTS member_since TIMESTAMP DEFAULT now(),
        ADD COLUMN IF NOT EXISTS last_seen TIMESTAMP DEFAULT now()
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()


# _______________________________


def downgrade(conn, **kwargs):
    query = """
        ALTER TABLE users
        DROP COLUMN IF EXISTS location,
        DROP COLUMN IF EXISTS about_me,
        DROP COLUMN IF EXISTS member_since,
        DROP COLUMN IF EXISTS last_seen
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
