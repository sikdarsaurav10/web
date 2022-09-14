from web.Admin.views import admin, admin_login_required
from web import db, app
from web.models import Admin_table, User_bookings, User_table
from flask import redirect, url_for, request, flash, jsonify
from web.utils import set_session
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import traceback
import string
import random
import json

@admin.route('/login', methods=['POST'])
def admin_login_submit():
    
    email = request.form['email']
    password = request.form['password']
    next_url = request.form['next']

    admin = Admin_table.query.filter_by(email=email.lower()).first()

    if not admin:
        flash('Email Does Not Exist. Contact Provider', 'danger')
        return redirect(url_for('admin.admin_login')), 200

    if not check_password_hash(admin.password, password):
        flash('Email or Password is not correct', 'warning')
        return redirect(url_for('admin.admin_login')), 301

    res = set_session('admin', admin.admin_id)
    if res:
        if next_url != '':
            return redirect(next_url)
        return redirect(url_for('admin.admin_index')), 301
    
    flash('Cannot Login at the moment', 'danger')
    return redirect(url_for('admin.admin_login')), 400


@admin.route('/create/api', methods=['POST'])
@admin_login_required
def admin_create_submit_api():
    
    res = request.get_json()
    email = res['email']
    password = res['password']
    name = res['name']

    admin = Admin_table.query.filter_by(email=email.lower()).first()

    if admin:
        return jsonify({'status': 0, 'message': 'Admin already exist'}), 200

    hashed_password = generate_password_hash(password,
                                             method='sha256')

    admin_id = str(uuid.uuid4())

    new = Admin_table(admin_id, email.lower(), hashed_password, name)

    try:
        db.session.add(new)
        db.session.commit()

        return jsonify({'status': 1, 'message': 'Admin Created'}), 200
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()

        return jsonify({'status': 0, 'message': 'Error'}), 400


@admin.route('/create', methods=['POST'])
@admin_login_required
def admin_create_submit():
    
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    name = request.form['name']

    if not email or not name:
        flash('Missing Inputs', 'warning')
        return redirect(url_for('admin.admin_create_view')), 301

    if password != confirm_password:
        flash('Password Does not Match', 'warning')
        return redirect(url_for('admin.admin_create_view')), 301

    admin = Admin_table.query.filter_by(email=email.lower()).first()

    if admin:
        flash('Admin already exist', 'warning')
        return redirect(url_for('admin.admin_create_view')), 301

    hashed_password = generate_password_hash(confirm_password,
                                             method='sha256')

    admin_id = str(uuid.uuid4())

    new = Admin_table(admin_id, email.lower(), hashed_password, name)

    try:
        db.session.add(new)
        db.session.commit()

        flash('Admin Created', 'success')
        return redirect(url_for('admin.admin_create_view')), 301
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()

        flash('Error', 'danger')
        return redirect(url_for('admin.admin_create_view')), 301

@admin.route('/update/post', methods=['POST'])
@admin_login_required
def admin_update_submit():
    
    admin_id = request.form['admin_id']
    name = request.form['name']

    admin = Admin_table.query.filter_by(admin_id=admin_id).first()

    if not admin:
        flash('Admin Does Not Exist', 'danger')
        return redirect(url_for('admin.admin_create_view')), 301

    admin.name = name

    try:
        db.session.commit()

        flash('Admin Updated', 'success')
        return redirect(url_for('admin.admin_create_view')), 301
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()

        flash('Error', 'danger')
        return redirect(url_for('admin.admin_create_view')), 301


@admin.route('/remove', methods=['POST'])
@admin_login_required
def admin_remove_submit():
    
    admin_id = request.form['admin_id']

    admin = Admin_table.query.filter_by(admin_id=admin_id).first()

    if not admin:
        flash('Admin Does Not Exist', 'danger')
        return redirect(url_for('admin.admin_create_view')), 301

    try:
        db.session.delete(admin)
        db.session.commit()

        flash('Admin Removed', 'success')
        return redirect(url_for('admin.admin_create_view')), 301
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()

        flash('Error', 'danger')
        return redirect(url_for('admin.admin_create_view')), 301


@admin.route('/create/user/post', methods=['POST'])
@admin_login_required
def admin_create_user_submit():
    
    email = request.form['email']
    password = request.form['password']
    contact = request.form['contact']
    confirm_password = request.form['confirm_password']
    name = request.form['name']

    if not email or not name or not contact:
        flash('Missing Inputs', 'warning')
        return redirect(url_for('admin.admin_create_user_view')), 301

    if password != confirm_password:
        flash('Password Does not Match', 'warning')
        return redirect(url_for('admin.admin_create_user_view')), 301

    user = User_table.query.filter((User_table.email == email.lower()) | (User_table.contact == contact)).first()

    if user:
        flash('User Email/Contact already exist', 'warning')
        return redirect(url_for('admin.admin_create_user_view')), 301

    hashed_password = generate_password_hash(confirm_password,
                                             method='sha256')

    alpha_num = string.ascii_letters + string.digits
    user_id = ''.join(random.choice(alpha_num) for i in range(5))

    new = User_table(user_id, email.lower(), hashed_password, name, contact)

    try:
        db.session.add(new)
        db.session.commit()

        flash('User Created', 'success')
        return redirect(url_for('admin.admin_create_user_view')), 301
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()

        flash('Error', 'danger')
        return redirect(url_for('admin.admin_create_user_view')), 301


@admin.route('/update/user/post', methods=['POST'])
@admin_login_required
def admin_update_user_submit():
    
    user_id = request.form['user_id']
    contact = request.form['contact']
    name = request.form['name']

    user = User_table.query.filter_by(user_id=user_id).first()

    user_con = User_table.query.filter((User_table.email != user.email) & (User_table.contact == contact)).first()

    if not user:
        flash('User Does Not Exist', 'danger')
        return redirect(url_for('admin.admin_create_user_view')), 301

    if user_con:
        flash('Contact Already exist', 'warning')
        return redirect(url_for('admin.admin_create_user_view')), 301

    user.name = name
    user.contact = contact

    try:
        db.session.commit()

        flash('User Updated', 'success')
        return redirect(url_for('admin.admin_create_user_view')), 301
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()

        flash('Error', 'danger')
        return redirect(url_for('admin.admin_create_user_view')), 301


@admin.route('/remove/user', methods=['POST'])
@admin_login_required
def admin_remove_user_submit():
    
    user_id = request.form['user_id']

    user = User_table.query.filter_by(user_id=user_id).first()

    if not user:
        flash('User Does Not Exist', 'danger')
        return redirect(url_for('admin.admin_create_user_view')), 301

    try:
        db.session.delete(user)
        db.session.commit()

        flash('User Removed', 'success')
        return redirect(url_for('admin.admin_create_user_view')), 301
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()

        flash('Error', 'danger')
        return redirect(url_for('admin.admin_create_user_view')), 301


@admin.route('/get/bookings/user', methods=['POST'])
@admin_login_required
def admin_user_data():
    
    if not request.is_json:
        flash('Something went wrong!', 'danger')
        return redirect(url_for('admin.admin_user_report_view')), 301

    user_id = request.get_json().get('user_id')

    user = User_table.query.filter_by(user_id=user_id).first()

    if not user:
        flash('User Does Not Exist', 'danger')
        return redirect(url_for('admin.admin_user_report_view')), 301

    bookings = User_bookings.query.filter_by(booking=user).all()
    # print(bookings)
    result = []
    for i in bookings:
        output = {}
        output["booking_id"] = i.booking_id
        output["destination"] = i.destination
        output["in_date"] = i.in_date
        output["out_date"] = i.out_date
        output["room_count"] = i.room_count
        output["people_count"] = i.people_count
        output["user_id"] = i.user_id

        result.append(output)

    return jsonify({"status": 1, "body": result}), 200


@admin.route('/get/user', methods=['POST'])
@admin_login_required
def admin_user_data_single():
    
    if not request.is_json:
        flash('Something went wrong!', 'danger')
        return redirect(url_for('admin.admin_user_report_view')), 301

    res = request.get_json()
    user_id = res['user_id']

    if request.get_json()['user_status']:
        user = User_table.query.filter_by(user_id=user_id).first()

        return jsonify({"status": 1, "body": {'email': user.email, 'name': user.name, 'contact': user.contact}}), 200
    else:
        user = Admin_table.query.filter_by(admin_id=user_id).first()

        return jsonify({"status": 1, "body": {'email': user.email, 'name': user.name}}), 200
