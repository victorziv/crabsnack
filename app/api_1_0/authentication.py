from flask import g, jsonify, current_app
from flask_httpauth import HTTPBasicAuth
from ..models import User, AnonymousUser
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')

    expiration = current_app.config['AUTH_TOKEN_EXPIRATION']
    return jsonify({
        'token': g.current_user.generate_auth_token(expiration=expiration),
        'expiration': expiration
    })


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True

    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None

    user = User().get_by_field(name='email', value=email_or_token)
    if not user:
        return False

    g.current_user = user
    g.token_used = False

    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')
