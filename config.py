import datetime

class Config(object):
    SECRET_KEY = 'hardcoded-key'
    FLASK_DEBUG = True
    MONGOALCHEMY_DATABASE = 'ams'

    # 5 months = 30 days * 5
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=150)
