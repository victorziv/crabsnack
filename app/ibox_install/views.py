from . import ibox_install
from flask import render_template


@ibox_install.route('/installation/steps')
def ibox_install_steps():
    return render_template('ibox/installation/steps.html')
