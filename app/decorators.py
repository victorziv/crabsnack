"""
Custom decorators that check user permissions
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

# ___________________________________


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_func
    return decorator
# ___________________________________


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
