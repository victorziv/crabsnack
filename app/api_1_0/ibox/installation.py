from flask import jsonify
from app.api_1_0 import api
from app.models import Installation
# ______________________________________


@api.route('/ibox/installation/steps/')
def get_ibox_installation_steps():
    steps = Installation().get_all()
    return jsonify({'steps': steps})
# ______________________________________
