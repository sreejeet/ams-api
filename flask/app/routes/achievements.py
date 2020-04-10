from flask import request
from flask_restful import Resource
import mongoalchemy
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import Achievement
from ..utils import convertToDate
from .. import api, URL_PREFIX


@api.resource(URL_PREFIX+'/achievements', URL_PREFIX+'/achievements/<id>', endpoint='achievements')
class AchievementResource(Resource):

    def get(self, id=None):
        """Return a achievement(s)"""

        try:
            # A unique achievement based on Object id
            if id:
                ach = Achievement.query.get(id)

                if not ach:
                    return {'msg':'Achievement not found'}, 404

                return {'data':ach.toDict()}, 200

            # Group of achievements based on filters
            filters = request.args.to_dict()
            if filters.get('date'):
                filters['date'] = convertToDate(filters['date'])

            achs = []
            for ach in Achievement.query.filter(filters).sort(('date',-1)).all():
                achs.append(ach.toDict())

            return {'data':achs}, 200

        except Exception as e:
            print(e)
            return {'msg':'Could not get achievements.'}, 500

    @jwt_required
    def delete(self, id=None):
        """Delete a single achievement"""

        if not id:
            return {'msg':'Missing achievement id.'}, 400

        try:
            ach = Achievement.query.get(id)
            if not ach:
                return {'msg':'Achievement not found'}, 404

            ach.remove()
            return {'msg':'Achievement deleted.'}, 200

        except Exception as e:
            print(e)
            return {'msg':'Could not delete achievement.'}, 500


    @jwt_required
    def put(self, id=None):
        """Modify all values of existsing achievement"""

        if not id:
            return {'msg':'Missing achievement id.'}, 400

        if not all(
            [request.form.get('title'),
            request.form.get('roll_no'),
            request.form.get('department'),
            request.form.get('semester'),
            request.form.get('date'),
            request.form.get('shift'),
            request.form.get('section'),
            request.form.get('session_from'),
            request.form.get('session_to'),
            request.form.get('venue'),
            request.form.get('category'),
            request.form.get('role'),
            request.form.get('name'),
            request.form.get('image_url'),
            request.form.get('approved'),
            request.form.get('description'),
            request.form.get('event_name'),]):

            return {'msg':'Field(s) missing.'}, 400

        try:
            ach = Achievement.query.get(id)

            if not ach:
                return {'msg':'Achievement not found'}, 404

            ach.title           = request.form.get('title')
            ach.roll_no         = request.form.get('roll_no')
            ach.department      = request.form.get('department')
            ach.semester        = int(request.form.get('semester'))
            ach.date            = convertToDate(request.form.get('date'))
            ach.shift           = request.form.get('shift')
            ach.section         = request.form.get('section')
            ach.session_from    = int(request.form.get('session_from'))
            ach.session_to      = int(request.form.get('session_to'))
            ach.venue           = request.form.get('venue')
            ach.category        = request.form.get('category')
            ach.role            = request.form.get('role')
            ach.name            = request.form.get('name')
            ach.image_url       = request.form.get('image_url')
            ach.approved        = request.form.get('approved').lower() == 'true'
            ach.description     = request.form.get('description')
            ach.event_name      = request.form.get('event_name')

            ach.save()
            return {'data' : ach.toDict()}, 200

        except (ValueError, mongoalchemy.exceptions.BadValueException) as e:
            print(e)
            return {'msg':'Invalid form data.'}, 400

        except Exception as e:
            print(e)
            return {'msg':'Could not modify achievement.'}, 500


@api.resource(URL_PREFIX+'/achievements')
class CreateAchievement(Resource):

    def post(self):
        """Add new non-academic achievement"""

        if not all(
            [request.form.get('title'),
            request.form.get('roll_no'),
            request.form.get('department'),
            request.form.get('semester'),
            request.form.get('date'),
            request.form.get('shift'),
            request.form.get('section'),
            request.form.get('session_from'),
            request.form.get('session_to'),
            request.form.get('venue'),
            request.form.get('category'),
            request.form.get('role'),
            request.form.get('name'),
            request.form.get('image_url'),
            request.form.get('approved'),
            request.form.get('description'),
            request.form.get('event_name'),]):

            return {'msg':'Field(s) missing.'}, 400

        try:
            ach = Achievement(
                title           = request.form.get('title'),
                roll_no         = request.form.get('roll_no'),
                department      = request.form.get('department'),
                semester        = int(request.form.get('semester')),
                date            = convertToDate(request.form.get('date')),
                shift           = request.form.get('shift'),
                section         = request.form.get('section'),
                session_from    = int(request.form.get('session_from')),
                session_to      = int(request.form.get('session_to')),
                venue           = request.form.get('venue'),
                category        = request.form.get('category'),
                role            = request.form.get('role'),
                name            = request.form.get('name'),
                image_url       = request.form.get('image_url'),
                approved        = request.form.get('approved').lower() == 'true',
                description     = request.form.get('description'),
                event_name      = request.form.get('event_name'),
            )

            ach.save()
            data = ach.toDict()

            return {'data': data}, 201

        except (ValueError, mongoalchemy.exceptions.BadValueException) as e:
            print(e)
            return {'msg':'Invalid form data.'}, 400

        except Exception as e:
            print(e)
            return {'msg':'Could not create achievement.'}, 500
