from flask import jsonify
from . import api
from ..models import User, Permission
from .decorators import permission_required

# ______________________________________


@api.route('/users/')
def get_users():
    users = User.get_all()
    return jsonify({'users': [user.to_json() for user in users]})

# ______________________________________


@api.route('/users/<int:id>')
@permission_required(Permission.ADMINISTER)
def get_user(id):
    user = User().get_by_field(name='id', value=id)
    return jsonify({'user': user.to_json()})

# ______________________________________
