from flask import request, jsonify
from flask_restful import Resource
from passlib.context import CryptContext
from flask_jwt_extended import create_access_token

from ..models import User
from .. import app, URL_PREFIX


def userAuth(email, password):
    """Validate credentials"""

    pwd_context = CryptContext(schemes=['bcrypt'])
    user = User.query.filter({'email':email}).first()

    if pwd_context.verify(password, user.password):
        return True

    return False


@app.route(URL_PREFIX+'/login', methods=['POST'])
def login():
    """Authenticate email/password and return user info and JWT"""

    if not all(
        [request.form.get('email'),
        request.form.get('password')]):

        return jsonify({'msg':'Field(s) missing.'}), 400

    if userAuth(request.form.get('email'), request.form.get('password')):
        data = User.query.filter({'email':request.form.get('email')}).first().toDict()
        data['access_token'] = create_access_token(identity=data.get('_id'))
        return jsonify({'data':data}), 200

    return jsonify({'msg':'Invalid credentials'}), 403
