#!/usr/bin/env python


def create_table_comments(conn):
    query = """
        CREATE TABLE IF NOT EXISTS comments (
            id serial PRIMARY KEY,
            body TEXT,
            body_html TEXT,
            commentdate TIMESTAMP WITHOUT TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            authorid INTEGER NOT NULL,
            postid INTEGER NOT NULL,
            UNIQUE(author_id, post_id)
            FOREIGN KEY authorid REFERENCES users(id),
            FOREIGN KEY postid REFERENCES posts(id)
        );
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def drop_table_comments(conn):

    query = """
        DROP TABLE IF EXISTS comments
    """

    params = ()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
# _______________________________


def upgrade(conn, **kwargs):
    create_table_comments(conn)

# _______________________________


def downgrade(conn, **kwargs):
    drop_table_comments(conn)
# _______________________________
