from web import app, db, ma
from datetime import datetime

# admin Table
class Admin_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.now)

    def __init__(self, admin_id, email, password, name, date_created=datetime.now):
        self.admin_id = admin_id
        self.email = email
        self.password = password
        self.name = name
        self.date_created = date_created


# User Table
class User_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(10))
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.now)
    bookings = db.relationship('User_bookings',
                               cascade='all,delete',
                               backref='booking',
                               lazy=True)

    def __init__(self, user_id, email, password, name, contact='0', date_created=datetime.now):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.name = name
        self.contact = contact
        self.date_created = date_created


# User Booking Table
class User_bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(50), unique=True, nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    in_date = db.Column(db.DateTime,nullable=False)
    out_date = db.Column(db.DateTime,nullable=False)
    room_count = db.Column(db.Integer, nullable=False)
    people_count = db.Column(db.Integer,  nullable=False)
    user_id = db.Column(db.String(50),
                        db.ForeignKey('user_table.user_id'),
                        nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.now())

    def __init__(self, booking_id, destination, in_date, out_date,room_count, people_count, user_id, date_created=datetime.now()):
        self.booking_id = booking_id
        self.destination = destination
        self.in_date = in_date
        self.out_date = out_date
        self.room_count = room_count
        self.people_count = people_count
        self.user_id = user_id
        self.date_created = date_created

# # Table Schemas
# class AdminSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'admin_id', 'email', 'password', 'name', 'date_created')


# admin_schema = AdminSchema()
# admin_schemas = AdminSchema(many=True)


# class Schema(ma.Schema):
#     class Meta:
#         fields = ('id', 'user_id', 'email', 'password', 'name', 'date_created')


# user_schema = Schema()
# user_schemas = Schema(many=True)


# class BookingsSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'booking_id', 'destination', 'in_date', 'out_date', 'room_count', 'people_count', 'date_created', 'user_id')


# user_booking_schema = BookingsSchema()
# user_booking_schemas = BookingsSchema(many=True)
