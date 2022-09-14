
class Development:
    SECRET_KEY = 'helloworld'
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost:3306/SimpleTest"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sikdarsaurav10@gmail.com'
    MAIL_PASSWORD = 'jtepakcqaaovldff'
    MAIL_DEFAULT_SENDER = 'sikdarsaurav10@gmail.com'
