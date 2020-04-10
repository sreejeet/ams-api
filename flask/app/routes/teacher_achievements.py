from flask import request
from flask_restful import Resource
import mongoalchemy
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

from ..models import User, TeacherAchievement
from ..utils import convertToDate
from .. import api, URL_PREFIX


@api.resource(URL_PREFIX+'/teacher_achievements', URL_PREFIX+'/teacher_achievements/<id>')
class TeacherAchievementResource(Resource):

    def get(self, id=None):
        """Return achievement(s)."""

        try:
            # A unique teacher achievement based on Object id
            if id:
                data = []
                data = User.query.get(id).toDict()
                data['achievements'] = []
                for ach in TeacherAchievement.query.filter({'user_id':ObjectId(id)}).all():
                    data['achievements'].append(ach.toDict())
                return {'data':data}, 200

            # Group of teacher achievements based on filters
            filters = request.args.to_dict()
            if filters.get('date'):
                filters['date'] = convertToDate(filters['date'])
            if filters.get('user_id'):
                filters['user_id'] = ObjectId(filters['user_id'])
            
            data = []
            user_ids = set()

            # Getting teachers with achievements
            for ach in TeacherAchievement.query.filter(filters).all():
                user_ids.add(ach.toDict().get('user_id'))

            # Getting teacher data
            for id in user_ids:
                user = User.query.get(id).toDict()
                del user['email']
                del user['usergroup']
                data.append(user)

            # Getting achievements of each user
            for user in data:
                filters['user_id'] = ObjectId(user.get('_id'))
                user['achievements'] = []
                for achievement in TeacherAchievement.query.filter(filters).sort(('date',-1)).all():
                    ach = achievement.toDict()
                    del ach['user_id']
                    user['achievements'].append(ach)

            return {'data':data}, 200

        except Exception as e:
            print(e)
            return {'msg':'Could not get teacher achievements.'}, 500

    @jwt_required
    def delete(self, id=None):
        """Delete a single teacher achievement."""

        if not id:
            return {'msg':'Missing achievement id.'}, 400

        try:
            ach = TeacherAchievement.query.get(id)
            if not ach:
                return {'msg':'Teacher achievement not found'}, 404
            if not ach.toDict().get('user_id') == get_jwt_identity():
                return {'msg':'Unauthorized'}, 401
            ach.remove()
            return {'msg':'Teacher achievement deleted.'}, 200

        except Exception as e:
            print(e)
            return {'msg':'Could not delete teacher achievement.'}, 500

    @jwt_required
    def put(self, id=None):
        """Modify all values of existsing teacher achievement."""

        if not id:
            return {'msg':'Missing achievement id.'}, 400

        if not all(
            [request.form.get('ta_type'),
            request.form.get('sub_type'),
            request.form.get('international'),
            request.form.get('topic'),
            request.form.get('published'),
            request.form.get('sponsored'),
            request.form.get('reviewed'),
            request.form.get('date'),
            request.form.get('description'),
            request.form.get('msi'),
            request.form.get('place'),]):

            return {'msg':'Field(s) missing.'}, 400

        try:
            ach = TeacherAchievement.query.get(id)

            if not ach:
                return {'msg':'Teacher achievement not found'}, 404

            ach.ta_type         = request.form.get('ta_type')
            ach.sub_type        = request.form.get('sub_type')
            ach.international   = request.form.get('international').lower() == 'true'
            ach.topic           = request.form.get('topic')
            ach.published       = request.form.get('published')
            ach.sponsored       = request.form.get('sponsored').lower() == 'true'
            ach.reviewed        = request.form.get('reviewed').lower() == 'true'
            ach.date            = convertToDate(request.form.get('date'))
            ach.description     = request.form.get('description')
            ach.msi             = request.form.get('msi').lower() == 'true'
            ach.place           = request.form.get('place')

            ach.save()
            return {'data' : ach.toDict()}, 200

        except (ValueError, mongoalchemy.exceptions.BadValueException) as e:
            print(e)
            return {'msg':'Invalid form data.'}, 400

        except Exception as e:
            print(e)
            return {'msg':'Could not modify teacher achievement.'}, 500


@api.resource(URL_PREFIX+'/teacher_achievements')
class CreateTeacherAchievement(Resource):

    @jwt_required
    def post(self):
        """Add new teacher achievement."""

        if not all(
            [request.form.get('ta_type'),
            request.form.get('sub_type'),
            request.form.get('international'),
            request.form.get('topic'),
            request.form.get('published'),
            request.form.get('sponsored'),
            request.form.get('reviewed'),
            request.form.get('date'),
            request.form.get('description'),
            request.form.get('msi'),
            request.form.get('place'),]):

            return {'msg':'Field(s) missing.'}, 400

        try:
            ach = TeacherAchievement(
                user_id         = get_jwt_identity(),
                ta_type         = request.form.get('ta_type'),
                sub_type        = request.form.get('sub_type'),
                international   = request.form.get('international').lower() == 'true',
                topic           = request.form.get('topic'),
                published       = request.form.get('published'),
                sponsored       = request.form.get('sponsored').lower() == 'true',
                reviewed        = request.form.get('reviewed').lower() == 'true',
                date            = convertToDate(request.form.get('date')),
                description     = request.form.get('description'),
                msi             = request.form.get('msi').lower() == 'true',
                place           = request.form.get('place'),
            )

            ach.save()
            data = ach.toDict()
            return {'data' : data}, 201

        except (ValueError, mongoalchemy.exceptions.BadValueException) as e:
            print(e)
            return {'msg':'Invalid form data.'}, 400

        except Exception as e:
            print(e)
            return {'msg':'Could not create teacher achievement.'}, 500


@api.resource(URL_PREFIX+'/teacher_achievements/teachers')
class ListTeachersWithAchievement(Resource):

    def get(self):
        """Return la ist of teachers who have achievement(s)."""

        try:
            data = []
            user_ids = set()

            for ach in TeacherAchievement.query.all():
                user_ids.add(ach.toDict().get('user_id'))

            for id in user_ids:
                user = User.query.get(id).toDict()
                del user['email']
                del user['usergroup']
                data.append(user)

            return {'data':data}, 200

        except Exception as e:
            print(e)
            return {'msg':'Could not get teacher achievements.'}, 500
