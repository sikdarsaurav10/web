from web.Users.views import user, user_login_required
from web import db, app
from web.models import User_bookings, User_table
from flask import redirect, url_for, request, flash
from web.utils import get_session_value, set_session, send_mail
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import traceback
import string
import random
from datetime import datetime
from datetime import date

@user.route('/login', methods=['POST'])
def user_login_submit():
    
    email = request.form['email']
    password = request.form['password']
    next_url = request.form['next']

    user = User_table.query.filter_by(email=email.lower()).first()

    if not user:
        flash('Please Register as Email does not exist', 'danger')
        return redirect(url_for('user.user_login')), 200

    if not check_password_hash(user.password, password):
        flash('Email or Password is not correct', 'warning')
        return redirect(url_for('user.user_login')), 301

    res = set_session('user', user.user_id)
    if res:
        if next_url != '' and next_url != 'http://127.0.0.1:5000/usr/new/user/register':
            return redirect(next_url)
        return redirect(url_for('user.user_index')), 301
    
    flash('Cannot Login at the moment', 'danger')
    return redirect(url_for('user.user_login')), 400


@user.route('/new/user/register', methods=['POST'])
def user_register_user_submit():
    
    email = request.form['email']
    password = request.form['password']
    contact = request.form['contact']
    confirm_password = request.form['confirm_password']
    name = request.form['name']

    if not email or not name or not contact:
        flash('Missing Inputs', 'warning')
        return redirect(url_for('user.user_register')), 301

    if password != confirm_password:
        flash('Password Does not Match', 'warning')
        return redirect(url_for('user.user_register')), 301

    user = User_table.query.filter((User_table.email == email.lower()) | (User_table.contact == contact)).first()

    if user:
        flash('User Email/Contact already exist', 'warning')
        return redirect(url_for('user.user_register')), 301

    hashed_password = generate_password_hash(confirm_password,
                                             method='sha256')

    alpha_num = string.ascii_letters + string.digits
    user_id = ''.join(random.choice(alpha_num) for i in range(5))

    new = User_table(user_id, email.lower(), hashed_password, name, contact)

    try:
        db.session.add(new)
        db.session.commit()

        flash('Registration Successfull! Please Login', 'success')
        return redirect(url_for('user.user_login')), 301
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()

        flash('Error', 'danger')
        return redirect(url_for('user.user_register')), 301


@user.route('/user/submit/booking', methods=['POST'])
@user_login_required
def user_booking_submit():
    

    destination = request.form['destination']
    in_date = request.form['in_date']
    out_date = request.form['out_date']
    rooms_count = request.form['rooms_count']
    people_count = request.form['people_count']

    in_date = date(int(in_date.split('/')[2]), int(in_date.split('/')[0]), int(in_date.split('/')[1]))
    out_date = date(int(out_date.split('/')[2]), int(out_date.split('/')[0]), int(out_date.split('/')[1]))

    if out_date < in_date:
        flash('Checkout date cannot less than Checkin date', 'warning')
        return redirect(url_for('user.user_index')), 301

    alpha_num = string.ascii_letters + string.digits
    book_id = ''.join(random.choice(alpha_num) for i in range(7))

    new = User_bookings(book_id, destination, in_date, out_date, int(rooms_count), int(people_count), get_session_value('user'))

    res = {}

    res['book_id'] = book_id
    res['destination'] = destination
    res['in_date'] = in_date
    res['out_date'] = out_date
    res['rooms_count'] = rooms_count
    res['people_count'] = people_count

    print(res)

    try:
        db.session.add(new)
        db.session.commit()

        send_mail(get_session_value('user'), res)
        
        return redirect(url_for('user.user_response_page')), 301
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()

        flash('Error', 'danger')
        return redirect(url_for('user.user_index')), 301

