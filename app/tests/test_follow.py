from app.models import User, Permission


def test_follow_link_creation():
    u = User.save(attrs=dict(email='frida@nowhere.com', password='getout', role='user', username='Frida Zandberg'))
    assert u.can(Permission.FOLLOW)
