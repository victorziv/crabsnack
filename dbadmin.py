import os
import datetime
import glob
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, AsIs
from flask import current_app
# ========================================


class DBAdmin(object):

    def __init__(self, conn=None, conf=None):
        self.conn = conn
        self.conf = conf
    # __________________________________________

    @staticmethod
    def createdb(conn, newdb, newdb_owner=None):
        """
        Creates a new DB.

        To successfully create a new DB
        2 pre-requisites should be fullfilled.

        * A connection to a default DB should be established
        * The connected user should have at least CREATEDB authorization

        Parameters
        ----------

        conn : DB connection object
            Pre-constructed connection.
            I.e. conn object is already connected to a "default" DB
            existing on the DB engine.

        newdb : str
            The new DB name.

        newdb_owner : str
            (Optional). The owner of the newly created DB.
            The required user has to exist on the DB engine.

        Returns
        -------
        None

        """
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        try:
            query = """CREATE DATABASE %(dbname)s WITH OWNER %(user)s"""
            params = {'dbname': AsIs(newdb), 'user': AsIs(newdb_owner)}
            cur.execute(query, params)
        except psycopg2.ProgrammingError as pe:
            if 'already exists' in repr(pe):
                pass
            else:
                raise
        finally:
            cur.close()
    # ___________________________________________

    @staticmethod
    def dropdb(conn, dbtodrop):
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        try:
            query = """DROP DATABASE IF EXISTS %(dbname)s"""
            params = {'dbname': AsIs(dbtodrop)}
            cur.execute(query, params)
        finally:
            cur.close()
    # ___________________________

    @staticmethod
    def connectdb(dburi):
        try:
            conn = psycopg2.connect(dburi)
            print("Connected: {}".format(conn))
            return conn
        except psycopg2.OperationalError as e:
            print("ERROR!: {}".format(e))
            if 'does not exist' in str(e):
                return
            else:
                raise
    # ___________________________

    def get_upgrade_versions(self, upto_version):
        # --------------------------
        def _compose_version(vfile):
            module = os.path.splitext(os.path.basename(vfile))[0]
            version, name = module.split('_', 1)
            return dict(name=name, module=module, version=version)
        # --------------------------

        versions_path = os.path.join(self.conf.BASEDIR, 'migrations/versions')
        vfiles = glob.iglob(os.path.join(versions_path, '[0-9]*.py'))
        print("Versions files: {}".format(vfiles))
        versions = sorted(
            [_compose_version(vfile) for vfile in vfiles],
            key=lambda x: int(x['version'])
        )
        print("Versions: {}".format(versions))
        return versions

    # ___________________________

    def db_upgrade(self, upto_version):
        print("Up to version: {}".format(upto_version))
        versions = self.get_upgrade_versions(upto_version)

        self.apply_versions(versions)
        self.insert_changelog_record(migration_file)
    # _____________________________

    def apply_versions(self, versions):
        for ver in versions:
    # _____________________________

    def create_changelog_table(self):
        """
        """

        query = """
            CREATE TABLE IF NOT EXISTS changelog (
                id serial PRIMARY KEY,
                name VARCHAR(64) UNIQUE,
                filenumber VARCHAR(4),
                dateapplied TIMESTAMP,
                comment VARCHAR(255)
            );
        """
        params = {}

        self.cur.execute(query, params)
        self.conn.commit()
    # _____________________________

    def create_table_roles(self):
        """
        class models.Role
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), unique=True)
        default = db.Column(db.Boolean, default=False, index=True)
        permissions = db.Column(db.Integer)
        """

        query = """
            CREATE TABLE IF NOT EXISTS roles (
                id serial PRIMARY KEY,
                name VARCHAR(64) UNIQUE,
                isdefault BOOLEAN DEFAULT FALSE,
                permissions INTEGER
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
                social_id VARCHAR(64) NOT NULL UNIQUE,
                nickname VARCHAR(64) NOT NULL,
                email VARCHAR(64) UNIQUE,
                username VARCHAR(64) UNIQUE,
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

    def drop_table(self, table):
        print("DB: %r" % self.__dict__)
        print("Table to drop: %r" % table)

        self.cur.execute("""
            DROP TABLE IF EXISTS %s CASCADE
        """ % table)

        self.conn.commit()

    # _____________________________

    def create_tables(self):
        tables = current_app.config['DB_TABLES_BASELINE']
        for table in tables:
            self.drop_table(table)
            getattr(self, "create_table_%s" % table)()
            self.grant_access_to_table(table)
    # ____________________________

    def create_baseline(self, conn):
        version = '0000'
        name = 'baseline'
        import importlib
        module_name = 'migrations.versions.{}_{}'.format(version, name)
        mod = importlib.import_module(module_name)
        mod.upgrade(conn, version, name)
    # _____________________________

    def drop_all(self):
        for table in self.all_tables:
            self.drop_table(table)
    # _____________________________

    def init_app(self, app):
        self.conn = DBAdmin.connectdb(app.config['DB_CONN_URI'])
        app.db = self
        app.db.cur = self.conn.cursor(cursor_factory=DictCursor)
        return app
    # _____________________________

    def db_downgrade(db):
        migrationdir = './migrations'
        migration_file = '0001.create_table-installationstep.sql'
        f = open(os.path.join(migrationdir, migration_file))
        try:
            db.cur.execute(f.read())
            db.conn.commit()
        except Exception:
            db.conn.rollback()
            return
        finally:
            f.close()
    # _____________________________

    def insert_changelog_record(self, version_number, name):

        """
        """
        try:

            query = """
                INSERT INTO changelog
                (version, name, applied)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """
            params = (version_number, name, datetime.datetime.now())

            self.cur.execute(query, params)
            self.conn.commit()
            fetch = self.cur.fetchone()
            return fetch['id']

        except Exception as e:
            print('ERROR: %s' % e)
            self.conn.rollback()
            return
# ____________________________


# class Baseline(object):

#     def __init__(self, db):
#         self.db = db

    # ____________________________

#     def create_tables(self):
#         tables = current_app.config['DB_TABLES_BASELINE']
#         for table in tables:
#             self.db.drop_table(table)
#             getattr(self.db, "create_table_%s" % table)()
#             self.db.grant_access_to_table(table)
    # ____________________________

#     def insert_base_version(self):

#         """
#         """

#         query = """
#             INSERT INTO changelog
#                 (version, name, applied)
#             VALUES (%s, %s, %s)
#             RETURNING id
#         """

#         params = (
#             '0000',
#             'initial_baseline',
#             datetime.datetime.now()
#         )

#         try:
#             self.db.cur.execute(query, params)
#             self.db.conn.commit()
#             fetch = self.db.cur.fetchone()
#             return fetch['id']

#         except IntegrityError as ie:
#             print('ERROR: %s' % ie)
#             self.db.conn.rollback()
#             return
#         except DatabaseError as dbe:
#             print('ERROR: %s' % dbe)
#             self.db.conn.rollback()
#             return
#     ____________________________

# def set_baseline():

#     """ Run deployment tasks. """

#     current_app.db.create_baseline()
#     Role().insert_roles()
#     User().insert_initial_users()
#     InstallationStep.insert_steps()
# _____________________________

# @manager.command
# def dbmigrate(configkey):
#     print("Config key %r" % configkey)
#     app = create_app(configkey)
#     app_context = app.app_context()
#     app_context.push()
#     connection_params = app.config['POSTGRES_CONNECTION_PARAMS']

#     app.db = DBAdmin()
#     try:
#         conn, cursor = app.db.connectdb(**connection_params)
#         upgradedb(app.db)
#     except Exception:
#         conn.rollback()
#     finally:
#         app_context.pop()
#         cursor.close()
#         conn.close()
