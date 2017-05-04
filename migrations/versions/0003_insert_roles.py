#!/usr/bin/env python

class Permission:
    FOLLOW = 0x01          # 0b00000001
    COMMENT = 0x02             # 0b00000010
    WRITE_ARTICLES = 0x04       # 0b00000100
    MODERATE_COMMENTS = 0x08  # 0b00001000
    ADMINISTER = 0x80           # 0b10000000

# ===========================


def insert_roles():
    roles = {
        'external_user': (
            Permission.FOLLOW,
            Permission.COMMENT, False),

        'user': (Permission.FOLLOW |
                 Permission.COMMENT |
                 Permission.WRITE_ARTICLES, True),

        'moderator': (
            Permission.FOLLOW |
            Permission.COMMENT |
            Permission.WRITE_ARTICLES |
            Permission.MODERATE_COMMENTS, False),

        'admin': (0xff, False)
    }

    for r in roles:
        role = read_one_by_field(name=r)
        print("Role found: %r ", role)
        if role is None:
            role = dict(
                name=r,
                permissions=roles[r][0],
                default=roles[r][1]
            )

            self.query.create(role)



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
