from app import create_app
from app.models import User


class TestFollow:

    @classmethod
    def setup_class(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
    # ______________________________

    @classmethod
    def teardown_class(cls):
        cls.app_context.pop()

    # ______________________________

    def test_follow_link_creation(self):
        u1 = User.save(attrs=dict(email='frida@nowhere.com', password='getout', role='user', username='Frida Zandberg'))
        u2 = User.save(attrs=dict(email='peppo@hereandnow.com', password='getin', role='user', username='Peppo Tocci'))
        u1.follow(u2)
        assert u1.is_following(u2)
