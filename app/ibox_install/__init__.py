from flask import Blueprint
ibox_install = Blueprint('ibox_install', __name__)

from . import views
