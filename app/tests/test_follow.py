from app.models import User, Permission


def test_follow_link_creation():
    u1 = User.save(attrs=dict(email='frida@nowhere.com', password='getout', role='user', username='Frida Zandberg'))
    u2 = User.save(attrs=dict(email='peppo@hereandnow.com', password='getin', role='user', username='Peppo Tocci'))
    assert u1.can(Permission.FOLLOW)
    assert u2.can(Permission.FOLLOW)
