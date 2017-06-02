from datetime import datetime
from flask import (
    render_template,
    redirect,
    url_for,
    abort,
    flash,
    request,
    current_app
)
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from ..models import Permission, User, Role, Post, Follow
from ..decorators import admin_required, permission_required
# _______________________________


@main.route('/blog', methods=['GET', 'POST'])
@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()

    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        Post.save(body=form.body.data, author=current_user._get_current_object())
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('page_size', current_app.config['POSTS_PER_PAGE'], type=int)

    offset = (per_page * page) - per_page
    posts = Post.get_all(offset=offset, limit=per_page)
    return render_template('index.html', form=form, posts=posts)
# _______________________________


@main.route('/post/<int:id>')
def post_by_id(id):
    posts = Post.get_by_field_or_404(name='id', value=id)
    return render_template('post.html', posts=posts)
# _______________________________


@main.route('/profile/edit/<int:id>', methods=['GET', 'POST'])
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


@main.route('/follow/<email>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(email):
    u = User.get_by_field(name='email', value=email)
    if u is None:
        flash("Invalid user")
        return redirect(url_for('.index'))
    if current_user.is_following(u):
        flash("You're already following this user")
        return redirect(url_for('.user_profile', email=email))

    current_user.follow(u)
    flash("You're now following {}".format(u.email))
    return redirect(url_for('.user_profile', email=email))
# _______________________________


@main.route('/unfollow/<email>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(email):
    u = User.get_by_field(name='email', value=email)
    if u is None:
        flash("Invalid user")
        return redirect(url_for('.index'))

    if not current_user.is_following(u):
        flash("You're not following this user")
        return redirect(url_for('.user_profile', email=email))

    current_user.unfollow(u)
    flash("You stopped following {}".format(u.email))
    return redirect(url_for('.user_profile', email=email))
# _______________________________


@main.route('/followed_by/<email>')
def followed_by(email):
    u = User.get_by_field(name="email", value=email)
    if u is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('page_size', current_app.config['FOLLOWERS_PER_PAGE'], type=int)
    offset = (per_page * page) - per_page
    items = Follow.get_followers(follower_id=u.id, offset=offset, limit=per_page)
    followed_by = [{'user': item.follower, 'started_following': item.started_following} for item in items]
    return render_template('followers.html', user=u, title="Followed by", endpoint='.followers', follows=followed_by)
# _______________________________


@main.route('/followers_for/<email>')
def followers_for(email):
    u = User.get_by_field(name="email", value=email)
    if u is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('page_size', current_app.config['FOLLOWERS_PER_PAGE'], type=int)
    offset = (per_page * page) - per_page
    items = Follow.get_followers(followed_id=u.id, offset=offset, limit=per_page)
    follows = [{'user': item.follower, 'started_following': item.started_following} for item in items]
    return render_template('followers.html', user=u, title="Followers of", endpoint='.followers', follows=follows)
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
# _________________________________________________


@main.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def post_edit(id):
    post = Post.get_by_field_or_404(name='id', value=id)[0]
    print("Fetch post: {}".format(post.__dict__))
    if current_user.email != post.author.email and not current_user.can(Permission.ADMINISTER):
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        print("UUUUU Body to update: {}".format(post.body))
        Post.update(body=post.body, postid=post.id)
        flash('The post has been updated.')
        return redirect(url_for('main.post_by_id', id=post.id))

    form.body.data = post.body
    return render_template('post_edit.html', form=form)
