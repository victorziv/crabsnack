import os
from app import create_app
from dbadmin import DBAdmin
# ============================


class TestDBCreate:

    @classmethod
    def setup_class(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        if cls.app.db.conn is not None:
            cls.app.db.conn.close()

        cls.db = DBAdmin()
        cls.admin_conn = cls.db.connectdb(cls.app.config['DB_CONN_URI_ADMIN'])
        cls.db.createdb(cls.admin_conn, cls.app.config['DBNAME'], cls.app.config['DBUSER'])

    # ______________________________

    @classmethod
    def teardown_class(cls):
        cls.app_context.pop()
        cls.db.dropdb(cls.admin_conn, cls.app.config['DBNAME'])
    # ______________________________

    def test_reset_app_db(self):
        assert os.path.basename(self.admin_conn.dsn) == self.app.config['DBNAME_ADMIN']
        self.db.dropdb(self.admin_conn, self.app.config['DBNAME'])
        self.db.createdb(self.admin_conn, self.app.config['DBNAME'], self.app.config['DBUSER'])
