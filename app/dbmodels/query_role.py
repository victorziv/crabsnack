from __future__ import print_function
import inspect
from psycopg2 import DatabaseError, ProgrammingError
from psycopg2.extensions import AsIs

# ============================================


class QueryRole:
    def __init__(self, db):
        self.db = db
    # ____________________________

    def read_one_by_field(self, **kwargs):
        fname = inspect.currentframe().f_code.co_name

        if len(kwargs) != 1:
            raise RuntimeError(
                "%s accepts exactly one parameter for a field name" % fname)
        field = next(iter(kwargs.keys()))

        query = """
            SELECT
                id,
                name,
                isdefault,
                permissions
            FROM roles
            WHERE %s = %s
        """
        params = (AsIs(field), kwargs[field])

        try:
            self.db.cur.execute(query, params)

        except ProgrammingError as pe:
            print('ERROR: {}'.format(pe))
            return
        except DatabaseError as e:
            print('ERROR: %s' % e)
            self.db.conn.rollback()

        fetch = self.db.cur.fetchone()
        print("Fetch: {}".format(fetch))
        return fetch
    # ____________________________

    def read(self, **kwargs):
        raise RuntimeError("Not implemented")
    # ____________________________

    def create(self, record):
        """
        name = db.Column(db.String(64), unique=True)
        isdefault = db.Column(db.Boolean, default=False, index=True)
        permissions = db.Column(db.Integer)
        """

        query = """
            INSERT INTO roles (name, isdefault, permissions)
            VALUES (%s, %s, %s)
            RETURNING id
        """

        params = (record['name'], record['isdefault'], record['permissions'])

        try:
            self.db.cur.execute(query, params)
            self.db.conn.commit()
            fetch = self.db.cur.fetchone()
            return fetch['id']
        except DatabaseError as e:
            print('ERROR: %s' % e)
            self.db.conn.rollback()
            return
    # ____________________________

    def update(self, record):
        """
        name = db.Column(db.String(64), unique=True)
        isdefault = db.Column(db.Boolean, default=False, index=True)
        permissions = db.Column(db.Integer)
        """

        query = """
            UPDATE  roles
            SET
                isdefault = %s,
                permissions = %s
            WHERE name = %s
        """

        params = (record['isdefault'], record['permissions'], record['name'])

        try:
            self.db.cur.execute(query, params)
            self.db.conn.commit()
        except DatabaseError as e:
            print('ERROR: %s' % e)
            self.db.conn.rollback()
            return
    # ____________________________
