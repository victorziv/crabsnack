#!/usr/bin/env python


def alter_table_follow_rename_columns(conn):

    query1 = """
        ALTER TABLE IF EXISTS follow RENAME COLUMN follower_id TO following_id;
    """

    query2 = """
        ALTER TABLE IF EXISTS follow RENAME COLUMN followed_id TO followed_by_id;
    """
    params = ()
    cursor = conn.cursor()
    cursor.execute(query1, params)
    cursor.execute(query2, params)
    conn.commit()
# _______________________________


def restore_original_column_names(conn):

    query1 = """
        ALTER TABLE IF EXISTS follow RENAME COLUMN following_id TO follower_id;
    """
    query2 = """
        ALTER TABLE IF EXISTS follow RENAME COLUMN followed_by_id TO followed_id;
    """

    params = ()
    cursor = conn.cursor()
    cursor.execute(query1, params)
    cursor.execute(query2, params)
    conn.commit()
# _______________________________


def upgrade(conn, **kwargs):
    alter_table_follow_rename_columns(conn)

# _______________________________


def downgrade(conn, **kwargs):
    restore_original_column_names(conn)
# _______________________________
