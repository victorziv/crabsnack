import pytest  # noqa
from app.models import AnonymousUser, Role, User, Permission


def test_roles_and_permissions():
    Role.insert_roles()
    u = User(email='john@example.com', password='cat')
    assert u.can(Permission.WRITE_ARTICLES)
    assert not u.can(Permission.MODERATE_COMMENTS)
# ____________________________________


def test_anonymous_user():
    u = AnonymousUser()
    assert not u.can(Permission.FOLLOW)
