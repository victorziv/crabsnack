import inspect
from psycopg2 import DatabaseError, ProgrammingError, IntegrityError
from psycopg2.extensions import AsIs

# ============================================


class QueryUser(object):
    def __init__(self, db):
        self.db = db
    # ____________________________

    def read_one_by_field(self, **kwargs):
        fname = inspect.currentframe().f_code.co_name

        if len(kwargs) != 1:
            raise RuntimeError(
                "%s accepts exactly one parameter for a field name" % fname)

        field = next(kwargs.__iter__())

        query = """
            SELECT
                u.id,
                u.email,
                u.username,
                u.password_hash,
                r.name AS role,
                r.permissions
            FROM users AS u, roles AS r
            WHERE u.role_id = r.id
            AND u.%s = %s
        """

        params = (AsIs(field), kwargs[field])

        try:
            self.db.cur.execute(query, params)

        except DatabaseError as e:
            print('ERROR: %s' % e)
            self.db.conn.rollback()

        try:
            fetch = self.db.cur.fetchone()
        except ProgrammingError as pe:
            if 'no results to fetch' in repr(pe):
                return
            else:
                raise
        else:
            return fetch
    # ____________________________

    def read(self, **kwargs):
        query = """
            SELECT
                u.id,
                u.email,
                u.username,
                r.name AS role,
                r.permissions
            FROM users AS u, roles AS r
            WHERE u.role_id = r.id
        """
        params = ()

        try:
            self.db.cur.execute(query, params)

        except DatabaseError as e:
            print('ERROR: %s' % e)
            self.db.conn.rollback()

        fetch = self.db.cur.fetchall()
        if fetch is None:
            return fetch

        print("Read fetch: %r" % fetch)
        return fetch
    # ____________________________

    def create(self, email, username, password_hash, role_id):
        """
        id = SERIAL primary_key=True)
        email = String(64), unique=True, index=True
        username String(64), unique=True, index=True
        password = String(128), salted SHA1 hash
        role_id = ObjectId, db.ForeignKey('roles.id'))
        """

        query = """
            INSERT INTO users (email, username, password_hash, role_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """

        params = (email, username, password_hash, role_id)

        try:
            self.db.cur.execute(query, params)
            self.db.conn.commit()
            fetch = self.db.cur.fetchone()
            print("XXXXX==> FETCH: {}".format(fetch))
            return fetch['id']

        except IntegrityError as ie:
            print('ERROR: %s' % ie)
            self.db.conn.rollback()
            return
        except DatabaseError as dbe:
            print('ERROR: %s' % dbe)
            self.db.conn.rollback()
            return
    # ____________________________

    def remove_all_records(self):
        query = """
            DELETE FROM users
        """
        params = ()
        try:
            self.db.cur.execute(query, params)
            self.db.conn.commit()
        except DatabaseError as e:
            print('ERROR: %s' % e)
            self.db.conn.rollback()
            return
    # ____________________________
