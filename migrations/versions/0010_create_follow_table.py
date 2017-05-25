#!/usr/bin/env python


def create_table_follow(conn):
    query = """
        CREATE TABLE IF NOT EXISTS follow (
            follower_id INTEGER NOT NULL,
            followed_id INTEGER NOT NULL,
            started_following TIMESTAMP WITHOUT TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            PRIMARY KEY(follower_id, followed_id)
        );
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def drop_table_follow(conn):

    query = """
        DROP TABLE IF EXISTS follow
    """

    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def upgrade(conn, **kwargs):
    create_table_follow(conn)

# _______________________________


def downgrade(conn, **kwargs):
    drop_table_follow(conn)
# _______________________________
