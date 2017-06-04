#!/usr/bin/env python


def create_table_follow(conn):
    """
    Many-to-many relationship to users table - both for followers and followed
        follower_id INTEGER NOT NULL REFERENCES users,
        followed_id INTEGER NOT NULL REFERENCES users,

    Alternative to REFERENCES users is FOREIGN KEY:

         FOREIGN KEY(follower_id) REFERENCES users(id) ON DELETE CASCADE,
         FOREIGN KEY(followed_id) REFERENCES users(id) ON DELETE CASCADE
    Difference is in DELETE CASCADE. Figure out what it's about.
    """
    query = """
        CREATE TABLE IF NOT EXISTS follow (
            follower_id INTEGER NOT NULL,
            followed_id INTEGER NOT NULL,
            started_following TIMESTAMP WITHOUT TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            PRIMARY KEY(follower_id, followed_id),
            FOREIGN KEY(follower_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(followed_id) REFERENCES users(id) ON DELETE CASCADE
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
