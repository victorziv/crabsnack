from app import create_app
from app.models import User, Follow


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

    # ______________________________

    def test_unfollow(self):
        u3 = User.save(attrs=dict(email='maryp@nowhere.com', password='getout', role='user', username='Mary Popper'))
        u4 = User.save(attrs=dict(
            email='kristyb@hereandnow.com',
            password='getin',
            role='user',
            username='Kristy Balsamo'))
        u4.follow(u3)
        assert u4.is_following(u3)
        u4.unfollow(u3)
        assert Follow.get_by_field(name='followed_id', value=u3.id) is None
