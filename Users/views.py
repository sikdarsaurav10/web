from flask import Blueprint, render_template, redirect, url_for, flash,request, session
from web.models import User_bookings, User_table
from web.utils import get_session, unset_session, get_session_value
from functools import wraps

user = Blueprint('user', __name__)

def user_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session.keys():
            return redirect(url_for('user.user_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@user.route('/login', methods=['GET'])
def user_login():
    res = get_session('user')
    if res:
        return redirect(url_for('user.user_index')), 301
    title = 'User Login'
    return render_template('user/login.html', title=title)

@user.route('/registration', methods=['GET'])
def user_register():
    res = get_session('user')
    if res:
        return redirect(url_for('user.admin_index')), 301
    title = 'User Register'
    return render_template('user/register.html', title=title)


@user.route('/', methods=['GET'])
@user_login_required
def user_index():
    
    user = User_table.query.filter_by(user_id=get_session_value('user')).first()
    title = f'Welcome {user.name}'
    return render_template('user/index.html', title=title, name=user.name)


@user.route('/user/bookings', methods=['GET'])
@user_login_required
def user_bookings_view():
    
    user = User_table.query.filter_by(user_id=get_session_value('user')).first()
    title = f'Welcome {user.name} | Bookings'

    bookings = User_bookings.query.filter_by(booking=user).all()
    return render_template('user/all_bookings.html', title=title, bookings=bookings)


@user.route('/reponse/page', methods=['GET'])
@user_login_required
def user_response_page():
    
    
    title = f'Form Submitted!!'
    return render_template('user/response.html', title=title)


@user.route('/logout', methods=['GET'])
@user_login_required
def logout():
    res = unset_session('user')

    if res:
        flash('Logged Out!!', 'warning')
        return redirect(url_for('user.user_login')), 301