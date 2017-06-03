import pytest
from app import create_app
from app.models import User, Follow


class TestFollow:

    @classmethod
    def setup_class(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.save_users()
    # ______________________________

    @classmethod
    def save_users(cls):
        users = [
            dict(email='frida@nowhere.com', password='getout', role='user', username='Frida Zandberg'),
            dict(email='peppo@hereandnow.com', password='getin', role='user', username='Peppo Tocci'),
            dict(email='maryp@nowhere.com', password='getout', role='user', username='Mary Popper'),
            dict(email='kristyb@hereandnow.com', password='getin', role='user', username='Kristy Balsamo'),
            dict(email='zaz@nowhere.com', password='getout', role='user', username='Isabelle Geffroy'),
            dict(email='georgeb@hereandnow.com', password='getin', role='user', username='George Brassans')
        ]

        for uind, u in enumerate(users):
            setattr(cls, 'u{}'.format(uind + 1), User.save(attrs=u))
    # ______________________________

    @classmethod
    def teardown_class(cls):
        cls.app_context.pop()

    # ______________________________

    def test_follow_link_creation(self):
        self.u1.follow(self.u2)
        assert self.u1.is_following(self.u2)

    # ______________________________

    def test_unfollow(self):
        self.u4.follow(self.u3)
        assert self.u4.is_following(self.u3)
        self.u4.unfollow(self.u3)
        assert Follow.get_by_field(name='followed_id', value=self.u3.id) is None
    # ______________________________

    def test_follow_count_setter(self):
        self.u6.follow(self.u5)
        assert self.u6.is_following(self.u5)
        with pytest.raises(ValueError):
            self.u5.followers_count = 14
    # ______________________________

    def test_follow_count_getter(self):
        self.u1.follow(self.u5)
        self.u2.follow(self.u5)
        assert self.u1.is_following(self.u5)
        assert self.u2.is_following(self.u5)
        assert self.u5.followers_count == 2
    # ______________________________

    def test_followed_user(self):
        self.user_followed = User.get_by_field(name='email', value='zaz@nowhere.com')
        assert self.user_followed.email == 'zaz@nowhere.com'
        self.u1.follow(self.user_followed)
        assert self.u1.is_following(self.user_followed)
        self.u2.follow(self.user_followed)
        assert self.u2.is_following(self.user_followed)
    # ______________________________

    def test_is_following_by(self):
        print("Follower: {}".format(self.u1))
        print("Followed By: {}".format(self.u1))
        follower = self.u1
        followed_by = self.u2
        fields = [
            {'name': 'follower_id', 'value': follower.id},
            {'name': 'followed_id', 'value': followed_by.id},
        ]

        is_following = Follow.query.read_by_fields(fields)
        assert is_following
