#!/usr/bin/env python


from app.models import User


def upgrade(conn, **kwargs):
    u = User()
    u.insert_initial_users()

# _______________________________


def downgrade(conn, **kwargs):
    pass
