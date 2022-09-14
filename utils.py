from flask import session
from web import app, mail
from flask_mail import Message

def set_session(key, value):
    if key in session:
        return False
    session[key] = value
    return True

def get_session(key):
    if key in session:
        return True
    return False


def get_session_value(key):
    if key in session:
        return session[key]
    return False

def unset_session(key):
    if key in session:
        del session[key]
        return True
    return False


def send_mail(email, data):
    msg = Message('Booking Successfull!! with Simple',
                  recipients=[str(email)])
    
    msg.body = f'Your Booking for {data["destination"]} has been Booked Successfully! <br> Checkin date: {data["in_date"]} <br> Checkout date: {data["out_date"]}<br> Rooms Booked: {data["rooms_count"]} <br> People: {data["people_count"]}'

    mail.send(msg)
