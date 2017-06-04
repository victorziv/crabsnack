"""
A reference on how to check a table existence can be found here:
http://stackoverflow.com/questions/1874113/checking-if-a-postgresql-table-exists-under-python-and-probably-psycopg2

"""
from app.dbmodels.query_admin import DBAdmin
from config import config


class Test0001CreateUsersTable:
    def setup_class(cls):
        configkey = 'testing'
        cls.dba = DBAdmin(conf=config[configkey])

    def test_users_table_exists(self):
        assert False
