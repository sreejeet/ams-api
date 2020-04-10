from flask import Flask
from flask_restful import Api
from flask_mongoalchemy import MongoAlchemy
from flask_jwt_extended import JWTManager
import datetime
import os 


# Change as per requirement
# URL_PREFIX = '/api/v1'
URL_PREFIX = ''
INVITE_CODE = 'secret'

app = Flask(__name__)
# app.config.from_object(Config)
os.environ['FLASK_APP']

app.config['SECRET_KEY'] = os.environ['SECRET_KEY'] # 'hardcoded-key'
app.config['FLASK_DEBUG'] = os.environ['FLASK_DEBUG'] # True
app.config['MONGOALCHEMY_DATABASE'] = os.environ['MONGOALCHEMY_DATABASE'] # 'ams'
app.config['MONGOALCHEMY_SERVER'] = os.environ['MONGOALCHEMY_SERVER'] # 'mongo'
app.config['MONGOALCHEMY_PORT'] = os.environ['MONGOALCHEMY_PORT'] # 27017
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=150)
api = Api(app)
db = MongoAlchemy(app)
jwt = JWTManager(app)


from .models import *
from .routes.users import *
from .routes.achievements import *
from .routes.academics import *
from .routes.teacher_achievements import *
from .routes.actions import *


@app.route(URL_PREFIX+'/', methods=['GET'])
def home():
    return jsonify({'Server status':'Active'}), 200
