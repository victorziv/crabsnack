from psycopg2.extensions import AsIs


class Krabschema:

    def __init__(self, cur, conn):
        self.cur = cur
        self.conn = conn
    # ______________________________

    def create_table_roles(self):
        query = """
            CREATE TABLE IF NOT EXISTS roles (
                id serial PRIMARY KEY,
                name VARCHAR(64) UNIQUE,
                isdefault BOOLEAN DEFAULT FALSE,
                permissions INTEGER,
                location VARCHAR(64),
                about_me TEXT,
                member_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        params = {}

        self.cur.execute(query, params)
        self.conn.commit()
    # _____________________________

    def create_table_changelog(self):

        query = """
           CREATE TABLE IF NOT EXISTS changelog (
               id serial PRIMARY KEY,
               version VARCHAR(4),
               name VARCHAR(100) UNIQUE,
               applied TIMESTAMP
           );
        """
        params = {}

        self.cur.execute(query, params)
        self.conn.commit()
    # _____________________________

    def create_table_installationstep(self):
        """
        class models.InstallationStep
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(32), unique=True)
        display_name = db.Column(db.String(64), unique=True)
        priority = INTEGER
        """

        table = 'installationstep'

        query = """
            CREATE TABLE IF NOT EXISTS %(table)s (
                id serial PRIMARY KEY,
                name VARCHAR(32) UNIQUE,
                display_name VARCHAR(64),
                priority INTEGER
            );
        """
        params = {'table': AsIs(table)}

        self.cur.execute(query, params)
        self.conn.commit()

        # Create an index on priority column
        query = """ CREATE INDEX priority_ind ON %(table)s (priority); """
        params = {'table': AsIs(table)}

        self.cur.execute(query, params)
        self.conn.commit()
    # _____________________________

    def create_table_users(self):

        query = """
            CREATE TABLE IF NOT EXISTS users (
                id serial PRIMARY KEY,
                social_id VARCHAR(64) UNIQUE,
                username VARCHAR(128),
                email VARCHAR(64) UNIQUE,
                password_hash VARCHAR(128),
                role_id INTEGER REFERENCES roles(id)
            );
        """
        params = {}

        self.cur.execute(query, params)
        self.conn.commit()
    # _____________________________

    def grant_access_to_table(self, table):
        query = """GRANT ALL ON TABLE %(table)s TO %(user)s"""
        params = {'table': AsIs(table), 'user': AsIs('ivt')}

        self.cur.execute(query, params)
        self.conn.commit()

    # ___________________________
