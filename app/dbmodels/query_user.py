from psycopg2 import DatabaseError, ProgrammingError, IntegrityError
from psycopg2.extensions import AsIs
from psycopg2 import sql

# ============================================


class QueryUser(object):
    def __init__(self, db):
        self.db = db
    # ____________________________

    def read_one_by_field(self, **kwargs):

        if len(kwargs) != 1:
            raise RuntimeError("Accepts exactly one parameter for a field name")

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

    def create_oauth(self, email, username, social_id, role_id):
        """
        id = SERIAL primary_key=True)
        email = String(64), unique=True, index=True
        username String(64), unique=True, index=True
        password = String(128), salted SHA1 hash
        role_id = ObjectId, db.ForeignKey('roles.id'))
        """

        query = """
            INSERT INTO users (email, username, social_id, role_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """

        params = (email, username, social_id, role_id)

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
        self.db.cur.execute(query, params)
        self.db.conn.commit()
    # ____________________________

    def update(self, email, params):
        query = sql.SQL("""
            UPDATE users
            SET {} = %s
            WHERE {} = %s
        """).format(
            sql.Identifier('last_seen'),
            sql.Identifier('email'),
        )

        params = {params['last_seen'], email}
        self.db.cur.execute(query, params)
        self.db.conn.commit()
    # ____________________________
