import pytest
from app import create_app
from app.models import Role


class TestRoleModel:

    @classmethod
    def setup_class(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.password = 'mucho'
    # ______________________________

    @classmethod
    def teardown_class(cls):
        cls.app_context.pop()

    # ______________________________

    def test_role_queries_object(self):
        role = Role()
        assert hasattr(role, 'query')
        assert hasattr(role.query, 'db')
        assert hasattr(role.query.db, 'cur')
        assert type(role.query.db.cur).__name__ == 'DictCursor'

    # ______________________________

    def test_insert_roles(self):
        role = Role()
        role.insert_roles()
    # ______________________________

    def test_fetch_role(self):
        role = Role()
        admin = role.get_by_field(name='name', value='admin')
        print("Fetched role: %r" % admin)
        assert admin['name'] == 'admin'
