from api import db
from utils import convertFromDate


class User(db.Document):
    """User object model."""

    _id         = None
    firstname   = db.StringField()
    lastname    = db.StringField()
    designation = db.StringField()
    email       = db.StringField()
    password    = db.StringField()
    usergroup   = db.EnumField(db.StringField(), 'TEACHER','ADMIN')

    def toDict(self):
        data = self.wrap()
        data['_id'] = str(data['_id'])
        del data['password']
        return data


class Achievement(db.Document):
    """Non-academic Achivement object model."""

    _id             = None
    title           = db.StringField()
    roll_no         = db.StringField()
    department      = db.EnumField(db.StringField(), 'COMPUTERSCIENCE', 'EDUCATION', 'MANAGEMENT', 'COMMERCE')
    semester        = db.EnumField(db.IntField(), 1, 2, 3, 4, 5, 6)
    date            = db.DateTimeField()
    shift           = db.EnumField(db.StringField(), 'MORNING', 'EVENING')
    section         = db.EnumField(db.StringField(), 'A', 'B', 'C')
    session_from    = db.IntField()
    session_to      = db.IntField()
    venue           = db.StringField()
    category        = db.EnumField(db.StringField(), 'SPORTS', 'TECHNICAL', 'CULTURAL', 'OTHERS')
    role            = db.EnumField(db.StringField(), 'PARTICIPANT', 'COORDINATOR')
    name            = db.StringField()
    image_url       = db.StringField()
    approved        = db.BoolField()
    description     = db.StringField()
    event_name      = db.StringField()

    def toDict(self):
        data = self.wrap()
        data['date'] = convertFromDate(data['date'])
        data['_id'] = str(data['_id'])
        return data


class AcademicAchievement(db.Document):
    """Academic Achivement object model."""

    _id         = None
    roll_no     = db.StringField()
    name        = db.StringField()
    batch       = db.StringField()
    programme   = db.EnumField(db.StringField(), 'B. Ed.', 'BBA (H) 4 years', 'BBA (General)', 'BBA (B&I)', 'BBA (T&TM)', 'BCA', 'B.Com (H)')
    category    = db.EnumField(db.StringField(), 'GOLDMEDALIST', 'EXEMPLARY', 'BOTH')

    def toDict(self):
        data = self.wrap()
        data['_id'] = str(data['_id'])
        return data


class TeacherAchievement(db.Document):
    """Teacher achivement object model."""

    _id             = None
    user_id         = db.ObjectIdField()
    ta_type         = db.EnumField(db.StringField(), 'BOOK', 'JOURNAL', 'CONFERENCE', 'SEMINARATTENDED')
    sub_type        = db.EnumField(db.StringField(), 'SEMINAR', 'CONFERENCE', 'WORKSHOP', 'FDP', 'FDP1WEEK')
    international   = db.BoolField()
    topic           = db.StringField()
    published       = db.StringField()
    sponsored       = db.BoolField()
    reviewed        = db.BoolField()
    date            = db.DateTimeField()
    description     = db.StringField()
    msi             = db.BoolField()
    place           = db.StringField()

    def toDict(self):
        data = self.wrap()
        data['_id'] = str(data['_id'])
        data['user_id'] = str(data['user_id'])
        data['date'] = convertFromDate(data['date'])
        return data
