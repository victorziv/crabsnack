from flask import current_app

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
        current_app.logger.debug("Fields: {}".format(fields))
        values_placeholders = ', '.join(['%s' for v in attrs.values()])
        query = query_template.format(fields, values_placeholders)
        current_app.logger.debug("query: {}".format(query))
        current_app.logger.debug("values: {}".format(attrs.values()))
        params = tuple(attrs.values())

        current_app.logger.debug(self.db.cur.mogrify(query, params))

        self.db.cur.execute(query, params)
        self.db.conn.commit()
    # ____________________________
