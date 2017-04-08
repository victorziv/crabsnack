from flask import jsonify
from app.exceptions import ValidationError
from . import api

# _____________________________

def bad_request(message):
    response = jsonify({'error':'bad_request', 'message':message})
    response.status_code = 401
    return response

# _____________________________

def unauthorized(message):
    response = jsonify({'error':'unauthorized', 'message':message})
    response.status_code = 401
    return response
# _____________________________

def forbidden(message):
    response = jsonify({'error':'forbidden', 'message':message})
    response.status_code = 403
    return response
# _____________________________

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
