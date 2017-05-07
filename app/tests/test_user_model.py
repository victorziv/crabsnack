import pytest  # noqa
from app import create_app
from app.models import Role, User, AnonymousUser, Permission
# ====================================


class TestUserModel:

    @classmethod
    def setup_class(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.app.db.create_tables()
        cls.password = 'mucho'
        role = Role()
        role.insert_roles()
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

    def test_user(self):
        u = User()
        u.save_user(email='frida@nowhere.com', password='getout', role='user', username='Frida Zandberg')
        assert u.can(Permission.FOLLOW)
        assert u.can(Permission.WRITE_ARTICLES)
        assert not u.can(Permission.MODERATE_COMMENTS)
    # ______________________________

    def test_anonymous_user(self):
        u = AnonymousUser()
        assert not u.can(Permission.FOLLOW)
