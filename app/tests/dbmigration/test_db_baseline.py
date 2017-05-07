import os
from app import create_app
from dbadmin import DBAdmin
# ============================


class TestBaseline:

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

    def create_table(self):
        pass

    # ______________________________

    def test_valid_dbname(self):
        assert os.path.basename(self.admin_conn.dsn) == self.app.config['DBNAME_ADMIN']
        assert self.app.config['DBNAME'] != self.app.config['DBNAME_ADMIN']
    # ______________________________

    def test_create_baseline(self):
        self.create_table('ibox_installation')
