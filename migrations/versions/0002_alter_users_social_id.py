#!/usr/bin/env python


def upgrade(conn, **kwargs):
    try:
        query = """
            ALTER TABLE users
            ADD COLUMN IF NOT EXISTS social_id VARCHAR(64) UNIQUE;
        """
        params = ()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

    except Exception as e:
        print('ERROR: %s' % e)
        conn.rollback()
        return
# _______________________________


def downgrade(conn, **kwargs):
    try:
        query = """
            ALTER TABLE users DROP COLUMN IF EXISTS social_id;
        """
        params = ()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

    except Exception as e:
        print('ERROR: %s' % e)
        conn.rollback()
        return
