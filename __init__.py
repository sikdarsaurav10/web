from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_session import Session
from flask_mail import Mail
from web.config import Development

app = Flask(__name__)
app.config.from_object(Development)
app.jinja_env.filters['zip'] = zip

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
Session(app)
mail = Mail(app)

from web.Admin.views import admin
from web.Admin import routes
from web.Users.views import user
from web.Users import routes

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(user, url_prefix="/usr")