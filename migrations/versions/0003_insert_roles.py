#!/usr/bin/env python

from app.models import Role


def upgrade(conn, **kwargs):
    r = Role()
    r.insert_roles()

# _______________________________


def downgrade(conn, **kwargs):
    pass
