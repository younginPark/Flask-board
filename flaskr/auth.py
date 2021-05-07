import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import init_db
from flaskr.db import db_session
from flaskr.models import Users, Posts
from dataclasses import dataclass, asdict

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    print("레지스터 드렁옴")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        else:
            result = db_session.query(Users).filter(Users.username == username).all()
            if result:
                error = 'Error!!'
        if error is None:
            user_info = Users(username=username, password=generate_password_hash(password))
            db_session.add(user_info)
            db_session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db_session.query(Users).filter(Users.username == username).first()
        if not user:
            error = 'Incorrect Username or Password'
        else:
            user = user.__dict__
            if not check_password_hash(user['password'], password):
                error = 'Incorrect Username or Password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        tmp = db_session.query(Users).filter(Users.id == user_id).one()
        g.user = tmp.__dict__

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view