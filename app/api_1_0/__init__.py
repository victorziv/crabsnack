from flask import Blueprint
api = Blueprint('api', __name__)

from . import authentication  # noqa
from . import users  # noqa
from . import errors  # noqa
from .ibox import installation  # noqa
