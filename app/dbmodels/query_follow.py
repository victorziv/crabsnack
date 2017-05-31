from flask import current_app as cap
from psycopg2.extensions import AsIs

# ============================================


class QueryFollow(object):
    def __init__(self, db):
        self.db = db
    # ____________________________

    def create(self, attrs):

        query_template = """
            INSERT INTO follow ({})
            VALUES ({})
        """
        fields = ', '.join(attrs.keys())
        cap.logger.debug("Fields: {}".format(fields))
        values_placeholders = ', '.join(['%s' for v in attrs.values()])
        query = query_template.format(fields, values_placeholders)
        cap.logger.debug("query: {}".format(query))
        cap.logger.debug("values: {}".format(attrs.values()))
        params = tuple(attrs.values())

        cap.logger.debug(self.db.cursor.mogrify(query, params))

        self.db.cursor.execute(query, params)
        self.db.conn.commit()
    # ____________________________

    def read_one_by_field(self, **kwargs):

        field = next(iter(kwargs.keys()))

        query = """
            SELECT
                follower_id,
                followed_id,
                started_following
            FROM follow
            WHERE %s = %s
        """
        params = (AsIs(field), kwargs[field])
        self.db.cursor.execute(query, params)
        fetch = self.db.cursor.fetchone()
        cap.logger.debug("Fetch: {}".format(fetch))
        return fetch
    # ____________________________
