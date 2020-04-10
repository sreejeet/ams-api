from flask import request
from flask_restful import Resource
import mongoalchemy
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import AcademicAchievement
from ..utils import checkBatch
from .. import api, URL_PREFIX


@api.resource(URL_PREFIX+'/academics', URL_PREFIX+'/academics/<id>')
class AcademicAchievementResource(Resource):

    def get(self, id=None):
        """Return academic achievement(s)."""

        # A unique academic achievement based on Object id
        try:
            if id:
                ach = AcademicAchievement.query.get(id)
                if not ach:
                    return {'msg':'Academic achievement not found'}, 404

                return {'data':ach.toDict()}, 200

        # Group of academic achievements based on filters
            filters = request.args.to_dict()
            achs = []
            for ach in AcademicAchievement.query.filter(filters).sort(('batch',-1)).all():
                achs.append(ach.toDict())

            return {'data':achs}, 200

        except Exception as e:
            print(e)
            return {'msg':'Could not get academic achievement(s).'}, 500

    @jwt_required
    def delete(self, id=None):
        """Delete one academic achievement."""

        if not id:
            return {'msg':'Missing achievement id.'}, 400

        try:
            ach = AcademicAchievement.query.get(id)

            if not ach:
                return {'msg':'Academic achievement not found'}, 404

            ach.remove()
            return {'msg':'Academic achievement deleted.'}, 200

        except Exception as e:
            print(e)
            return {'msg':'Could not delete academic achievement.'}, 500

    @jwt_required
    def put(self, id=None):
        """Modify all values of existsing academic achievement."""

        if not id:
            return {'msg':'Missing achievement id.'}, 400

        if not all(
            [request.form.get('roll_no'),
            request.form.get('name'),
            request.form.get('batch'),
            request.form.get('programme'),
            request.form.get('category'),]):
        
            return {'msg':'Field(s) missing.'}, 400

        try:
            ach = AcademicAchievement.query.get(id)

            if not ach:
                return {'msg':'Academic achievement not found'}, 404

            ach.roll_no     = request.form.get('roll_no'),
            ach.name        = request.form.get('name'),
            ach.batch       = checkBatch(request.form.get('batch')),
            ach.programme   = request.form.get('programme'),
            ach.category    = request.form.get('category'),

            ach.save()
            data = ach.toDict()

            return {'data' : data}, 200

        except (ValueError, mongoalchemy.exceptions.BadValueException) as e:
            print(e)
            return {'msg':'Invalid form data.'}, 400

        except Exception as e:
            print(e)
            return {'msg':'Could not modify academic achievement.'}, 500


@api.resource(URL_PREFIX+'/academics')
class CreateAcademicAchievement(Resource):

    @jwt_required
    def post(self):
        """Add new academic achievement."""

        if not all(
            [request.form.get('roll_no'),
            request.form.get('name'),
            request.form.get('batch'),
            request.form.get('programme'),
            request.form.get('category'),]):

            return {'msg':'Field(s) missing.'}, 400

        try:
            ach = AcademicAchievement(
                roll_no     = request.form.get('roll_no'),
                name        = request.form.get('name'),
                batch       = checkBatch(request.form.get('batch')),
                programme   = request.form.get('programme'),
                category    = request.form.get('category'),
            )

            ach.save()
            data = ach.toDict()

            return {'data' : data}, 201

        except (ValueError, mongoalchemy.exceptions.BadValueException) as e:
            print(e)
            return {'msg':'Invalid form data.'}, 400

        except Exception as e:
            print(e)
            return {'msg':'Could not create academic achievement.'}, 500
