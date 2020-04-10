from flask import request
from flask_restful import Resource
from passlib.context import CryptContext
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import User
from .. import api, URL_PREFIX, INVITE_CODE


def userAuth(email, password):
    """Validate credentials"""

    pwd_context = CryptContext(schemes=['bcrypt'])
    user = User.query.filter({'email':email}).first()

    if pwd_context.verify(password, user.password):
        return True

    return False


@api.resource(URL_PREFIX+'/users', URL_PREFIX+'/users/<id>')
class UserIdResource(Resource):

    @jwt_required
    def get(self, id=None):
        """Return user info."""
        
        try:
            if not User.query.get(get_jwt_identity()).usergroup == 'ADMIN':
                return {'msg':'Unauthorised'}, 401

            if id:
                user = User.query.get(id)
                if not user:
                    return {'msg':'User not found'}, 404
                data = user.toDict()
            else:
                data = []
                for user in User.query.all():
                    data.append(user.toDict())

            return {'data':data}, 200

        except Exception as e:
            print(e)
            return {'msg':'Could not get user info.'}, 500

    @jwt_required
    def delete(self, id=None):
        """Delete a user based on user object id."""

        try:
            # If id is provided, check user is admin
            if id and (not User.query.get(get_jwt_identity()).usergroup == 'ADMIN'):
                return {'msg':'Unauthorised'}, 401

            user = User.query.get(id) if id else User.query.get(get_jwt_identity())
            if not user:
                return {'msg':'User not found.'}, 404
            user.remove()
            return {'msg':'User deleted.'}, 200

        except Exception as e:
            print(e)
            return {'msg':'Could not delete achievement.'}, 500


@api.resource(URL_PREFIX+'/users')
class UserResource(Resource):

    def post(self):
        """Check if user exists already, if not add new user."""

        if not all(
            [request.form.get('firstname'),
            request.form.get('lastname'),
            request.form.get('email'),
            request.form.get('password'),
            request.form.get('designation'),
            request.form.get('invite_code'),
            request.form.get('usergroup'),]):

            return {'msg':'Field(s) missing.'}, 400

        try:
            if not request.form.get('invite_code') == INVITE_CODE:
                return {'msg':'Incorrect invite code'}, 403

            if User.query.filter({'email':request.form.get('email')}).first():
                return {'msg':'Email already registered'}, 403

            pwd_context = CryptContext(schemes=['bcrypt'])
            pass_hash = pwd_context.hash(secret=request.form.get('password'))

            user = User(
                firstname   = request.form.get('firstname'),
                lastname    = request.form.get('lastname'),
                designation = request.form.get('designation'),
                email       = request.form.get('email'),
                usergroup   = request.form.get('usergroup'),
                password    = pass_hash,
            )

            user.save()
            return {'data' : user.toDict()}, 201

        except Exception as e:
            print(e)
            return {'msg':'Could not create user.'}, 500

    @jwt_required
    def put(self):
        """Update all values for current user."""

        if not all(
            [request.form.get('firstname'),
            request.form.get('lastname'),
            request.form.get('email'),
            request.form.get('password'),
            request.form.get('designation'),]):

            return {'msg':'Field(s) missing.'}, 400

        try:
            user = User.query.get(get_jwt_identity())

            user.firstname      = request.form.get('firstname')
            user.lastname       = request.form.get('lastname')
            user.designation    = request.form.get('designation')
            user.email          = request.form.get('email')

            user.save()
            return {'msg':'Updated', 'data':user.toDict()}, 200

        except Exception as e:
            print(e)
            return {'mgs':'Could not update user.'}, 500
