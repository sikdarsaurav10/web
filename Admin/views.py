from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from web.models import Admin_table, User_bookings, User_table
from web.utils import get_session, unset_session, get_session_value
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session.keys():
            return redirect(url_for('admin.admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/login', methods=['GET'])
def admin_login():
    res = get_session('admin')
    if res:
        return redirect(url_for('admin.admin_index')), 301
    title = 'Admin Login'
    return render_template('admin/login.html', title=title)


@admin.route('/', methods=['GET'])
@admin_login_required
def admin_index():

    title = 'Admin Dashboard'
    return render_template('admin/index.html', title=title)


@admin.route('/create/new', methods=['GET'])
@admin_login_required
def admin_create_view():

    title = 'Admin | Create Admin'
    admin = Admin_table.query.filter(Admin_table.admin_id != get_session_value('admin')).all()
    return render_template('admin/create_admin.html', title=title, admins=admin)


@admin.route('/create/user', methods=['GET'])
@admin_login_required
def admin_create_user_view():

    title = 'Admin | Create User'
    users = User_table.query.all()
    return render_template('admin/create_user.html', title=title, users=users)


@admin.route('/user/report', methods=['GET'])
@admin_login_required
def admin_user_report_view():

    title = 'Admin | User Report'
    users = User_table.query.all()
    result = {}
    for i in users:
        quer = len(User_bookings.query.filter_by(booking=i).all())
        result[i.id] = quer
    return render_template('admin/user_report.html', title=title, users=users, result=result)

@admin.route('/bookings/all', methods=['GET'])
@admin_login_required
def admin_all_bookings_view():

    title = 'Admin | All Bookings'
    bookings = User_bookings.query.all()
    return render_template('admin/all_user_bookings.html', title=title, bookings=bookings)


@admin.route('/logout', methods=['GET'])
def admin_logout():
    res = unset_session('admin')
    if res:
        flash('Logged Out!!', 'warning')
        return redirect(url_for('admin.admin_login')), 301