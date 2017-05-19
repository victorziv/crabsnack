from flask import current_app
from psycopg2.extensions import AsIs

# ============================================


class QueryPost(object):
    def __init__(self, db):
        self.db = db
    # ____________________________

    def read(self, sort_by, sort_order, offset, limit):
        query = """
            SELECT
                p.id,
                p.body,
                p.postdate,
                u.username,
                u.email,
                u.avatar_hash
            FROM posts AS p, users AS u
            WHERE p.authorid = u.id
            ORDER BY %s %s
            OFFSET %s
        """
        params = [AsIs(sort_by), AsIs(sort_order), AsIs(offset)]

        if limit is not None:
            query += 'LIMIT %s'
            params.append(AsIs(limit))

        self.db.cur.execute(query, params)
        fetch = self.db.cur.fetchall()
        if fetch is None:
            return fetch

        current_app.logger.debug("Fetch: {}".format(fetch))
        return fetch
    # ____________________________

    def create(self, attrs):
        """
        """

        body = attrs['body']
        authorid = attrs['authorid']
        postdate = attrs.get('postdate')

        if postdate is not None:
            query = """
                INSERT INTO posts (body, postdate, authorid)
                VALUES (%s, %s, %s)
                RETURNING id
            """
            params = (body, postdate, authorid)
        else:
            query = """
                INSERT INTO posts (body, authorid)
                VALUES (%s, %s)
                RETURNING id
            """

            params = (body, authorid)

        self.db.cur.execute(query, params)
        self.db.conn.commit()
        fetch = self.db.cur.fetchone()
        return fetch['id']

    # ____________________________

    def remove_all_records(self):
        query = """
            DELETE FROM posts
        """
        params = ()
        self.db.cur.execute(query, params)
        self.db.conn.commit()
    # ____________________________

    def update(self, update_key_name, update_key_value, update_params):
        sql_template = "UPDATE users SET ({}) = %s WHERE {} = %s"
        query = sql_template.format(', '.join(update_params.keys()), update_key_name)
        params = (tuple(update_params.values()), update_key_value)
        print(self.db.cur.mogrify(query, params))
        self.db.cur.execute(query, params)
        self.db.conn.commit()
    # ____________________________
