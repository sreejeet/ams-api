from flask import Flask
from flask_restful import Api
from flask_mongoalchemy import MongoAlchemy
from flask_jwt_extended import JWTManager

from config import Config


# Change as per requirement
# URL_PREFIX = '/api/v1'
URL_PREFIX = ''
INVITE_CODE = 'secret'

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db = MongoAlchemy(app)
jwt = JWTManager(app)


if __name__ == '__main__':
    
    from models import *
    from routes.users import *
    from routes.achievements import *
    from routes.academics import *
    from routes.teacher_achievements import *
    from routes.actions import *


    @app.route(URL_PREFIX+'/', methods=['GET'])
    def home():
        """Return server status."""

        return jsonify({'Server status':'Active'}), 200


    app.run(debug=True)
