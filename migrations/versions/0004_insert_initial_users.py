#!/usr/bin/env python

USERS = [
    {
        'email': 'bobo@infinidat.com',
        'username': 'Bobo Mintz',
        'password': '1234'
    },
    {
        'email': 'vziv@infinidat.com',
        'username': 'Victor Ziv',
        'role': 'admin',
        'password': '1234'
    }
]


def upgrade(conn, **kwargs):

    try:
        query = """
            INSERT INTO users ( email, username, password, roleid )
            %s, %s, %s,
            SELECT id FROM roles WHERE name = %s
        """
        for user in USERS:
            params = (user['email'], user['username'], user['password'], user['role'])
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    except Exception as e:
        print('ERROR: %s' % e)
        conn.rollback()
        return
# _______________________________


def downgrade(conn, **kwargs):
    query = """
        DELETE FROM users WHERE email = %s
    """
    try:
        for user in USERS:
            params = (user['email'])
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    except Exception as e:
        print('ERROR: %s' % e)
        conn.rollback()
        return
