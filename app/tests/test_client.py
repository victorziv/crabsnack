from flask import url_for
from app import create_app
from app.models import User, Role

class TestFlaskWebClient:

    @classmethod
    def setup_class(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.app.db.create_all()
        Role.set_query()
        Role.insert_roles()

    def setup(self):
        self.client = self.app.test_client(use_cookies=True)

    @classmethod
    def teardown_class(cls):
        cls.app.db.drop_all()
        cls.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        data = response.get_data(as_text=True)
        assert('Stranger' in data)
