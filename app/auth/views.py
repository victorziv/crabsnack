from flask import render_template, redirect, request, url_for, flash
from flask import current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .oauth import OAuthSignIn
from ..models import User
from .forms import LoginForm, RegistrationForm
# __________________________________________


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.update_last_seen()
# __________________________________________


@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        redirect(url_for('main.index'))

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()
# __________________________________________


@auth.route('/callback/<provider>')
def oauth_callback(provider):

    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()

    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('main.index'))

    user = User().get_by_field(name='social_id', value=social_id)
    if not user:
        user = User().save_user_oauth(social_id=social_id, username=username, email=email)

    login_user(user, True)
    return redirect(url_for('main.index'))
# __________________________________________


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        app.logger.debug("Trying to fetch user by email: %r", form.email.data)
        user = User().get_by_field(name='email', value=form.email.data)
        app.logger.debug("User found: %r", user)
        app.logger.debug("User type: {}".format(type(user)))

        if user is not None and hasattr(user, 'id') and user.password_hash and user.verify_password(form.password.data):  # noqa
            app.logger.debug("User {} is verified".format(user))
            app.logger.debug("User {} session will be kept? {}".format(user, form.remember_me.data))
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password')

    return render_template('auth/login.html', form=form)
# _______________________________


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        User().save_user(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
# _______________________________


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('main.index'))
# __________________________________________


# @auth.route('/reset', methods=['GET', 'POST'])
# def password_reset_request():
#     if not current_user.is_anonymous:
#         return redirect(url_for('main.index'))
#     form = PasswordResetRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             token = user.generate_reset_token()
#             send_email(user.email, 'Reset Your Password',
#                        'auth/email/reset_password',
#                        user=user, token=token,
#                        next=request.args.get('next'))
#         flash('An email with instructions to reset your password has been '
#               'sent to you.')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password.html', form=form)
