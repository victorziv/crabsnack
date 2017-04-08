from flask import request, jsonify
from flask import current_app as app
from flask import render_template
from . import main

# ______________________________


@main.app_errorhandler(404)
def page_not_found(e):

    """
    The initial setup is to return JSON response
    only if the client accepts JSON ONLY.

      if request.accept_mimetypes.accept_json
          and not request.accept_mimetypes.accept_html:

    But for command line client this is not always the case.
    HTTPie client for example while using
        --json flag set Accept: header to "appclication/json,*.*".
    Regarding this the Flask server returns HTML page
        to the command-line client request which is pretty much useless.
    """
    if request.accept_mimetypes.accept_json:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        app.logger.error('!ERROR: Not found: %r', e)
        return response
    return render_template('404.html'), 404

# ______________________________


@main.app_errorhandler(500)
def internal_server_error(e):
    """
    Similar to 404 handler
    if request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html:
    """

    if request.accept_mimetypes.accept_json:
        response = jsonify({'error': 'server error'})
        response.status_code = 500
        app.logger.exception('!ERROR')
        return response
    return render_template('500.html'), 500
