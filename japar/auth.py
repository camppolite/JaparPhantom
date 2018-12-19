import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from japar.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with get_db().cursor() as cursor:
            cursor.execute(
                'SELECT * FROM thedoor WHERE id = %s', (user_id,)
            )
            g.user = cursor.fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username or not password:
            error = 'Username or Password is required.'
        elif len(username) > 512:
            error = 'Username is longer than 255.'
        elif len(password) > 512:
            error = 'Password is longer than 255.'
        else:
            with get_db().cursor() as cursor:
                cursor.execute(
                    'SELECT id FROM thedoor WHERE door_name = %s', (username,)
                )
                repeat = cursor.fetchone()
            if repeat is not None:
                error = 'User {0} is already registered.'.format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            with get_db().cursor() as cursor:
                cursor.execute(
                    'INSERT INTO thedoor (door_name, door_pwd) VALUES (%s, %s)',
                    (username, generate_password_hash(password))
                )
                get_db().commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        with get_db().cursor() as cursor:
            cursor.execute(
                'SELECT * FROM thedoor WHERE door_name = %s', (username,)
            )
            user = cursor.fetchone()

        if user is None or not check_password_hash(user['door_pwd'], password):
            error = 'Incorrect username or password.'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('auth.login'))
