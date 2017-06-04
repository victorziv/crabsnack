import os
from app import create_app
from app.dbmodels.query_admin import DBAdmin


class TestDBConnection:

    @classmethod
    def setup_class(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        if cls.app.db.conn is not None:
            cls.app.db.conn.close()
        cls.dbadmin = DBAdmin()
        cls.admin_conn = cls.dbadmin.connectdb(cls.app.config['DB_CONN_URI_ADMIN'])
        cls.dbadmin.createdb(cls.admin_conn, cls.app.config['DBNAME'], cls.app.config['DBUSER'])
    # ______________________________

    @classmethod
    def teardown_class(cls):
        cls.app_context.pop()
        cls.dbadmin.dropdb(cls.admin_conn, cls.app.config['DBNAME'])
    # ______________________________

    def test_connect_admin_db(self):
        conn = self.dbadmin.connectdb(self.app.config['DB_CONN_URI_ADMIN'])
        assert type(conn).__name__ == 'connection'
        assert conn.status == 1
        connected_dbname = os.path.basename(conn.dsn)
        assert connected_dbname == self.app.config['DBNAME_ADMIN']
    # ______________________________

    def test_connect_app_db(self):
        conn = self.dbadmin.connectdb(self.app.config['DB_CONN_URI'])
        assert type(conn).__name__ == 'connection'
        assert conn.status == 1
        assert self.app.config['DBNAME'] == os.path.basename(conn.dsn)

    # ______________________________
