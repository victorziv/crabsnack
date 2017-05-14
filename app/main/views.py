from datetime import datetime
from flask import (
    render_template,
    session, redirect,
    url_for, abort, flash,
)
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from flask_login import login_required, current_user
from ..models import Permission, User, Role
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


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.get_by_field_or_404(name='id', value=id)
    form = EditProfileAdminForm(user=user)

    if form.validate_on_submit():
        userd = dict(
            email=form.email.data,
            username=form.username.data,
            role=Role.get_by_field(name='name', value=form.role.data),
            location=form.location.data,
            about_me=form.about_me.data,
        )
        User.update_user(params=userd)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))

    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
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
# _______________________________


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.update_user({
            'email': current_user.email,
            'username': current_user.username,
            'location': current_user.location,
            'about_me': current_user.about_me
        })
        flash('Your profile has been updated.')
        return redirect(url_for('.user_profile', email=current_user.email))

    form.username.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
