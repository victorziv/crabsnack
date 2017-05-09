from datetime import datetime
from flask import render_template, session, redirect, url_for, abort
from . import main
from .forms import NameForm
from flask_login import login_required
from ..models import Permission, User
from ..decorators import admin_required, permission_required
# _______________________________


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # ...
        return redirect(url_for('.index'))

    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False),
        current_time=datetime.utcnow()
    )

# _______________________________


@main.route('/admin')
@login_required
@admin_required
def admin_site():
    return "For administrators only"

# _______________________________


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_comment():
    return "Yep, throw that schmuck away!"
# _______________________________


@main.route('/user/<email>')
def user_profile(email):
    u = User().get_by_field(name='email', value=email)
    if u is None:
        abort(404)
    return render_template('user_profile.html', user=u, current_time=datetime.utcnow())
