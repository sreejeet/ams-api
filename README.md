# ams-api
An improved API for the MSI Achievement Management System, built using
- Flask
- Flask-RESTFul
- Flask-JWT-Extended
- Flask-MongoAlchemy

To run, type
```sh
$ python3 api.py
OR
$ python api.py
```


This is a rough documentation.
In case of any discrepancy, please create an issue or pull request on the github repository.
All fields are of string type unless stated otherwise.
JSON Web Tokens are to be sent in the request header in format:
&nbsp;&nbsp;&nbsp;&nbsp;```Authorization: Bearer <Token>```

Author: V S Sreejeet


Format guide:
```
	Resource / Action name [Resource / Action]
		resource field 1
		resource field 2

	/route
		HTTP_METHOD: method description
			[required fields, JWT requirement]
```

Api documentation
```
User [Resource]
	firstname
	lastname
	email
	password
	designation
	usergroup : enum ['TEACHER', 'ADMIN']
	invite_code (not part of user model)

	/users
		GET: get user info
			[JWT]
		POST: create new user
			[all values]
		PUT: update all values for current user
			[all values, JwT]
		DELETE: delete current user
			[JWT]

	/users/<id>
		GET: admins can get specific user info
			[JWT]
		DELETE: admins can delete other users too
			[JWT]


Non-academic Achievements [Resource]
	title
	roll_no
	department : enum ['COMPUTERSCIENCE', 'EDUCATION', 'MANAGEMENT', 'COMMERCE']
	semester : int enum [1, 2, 3, 4, 5, 6]
	date : format [YYYY-MM-DD]
	shift : enum ['MORNING', 'EVENING']
	section : enum ['A', 'B', 'C']
	session_from : int
	session_to : int
	venue
	category : enum ['SPORTS', 'TECHNICAL', 'CULTURAL', 'OTHERS']
	role : enum ['PARTICIPANT', 'COORDINATOR']
	name
	image_url
	approved : bool
	description
	event_name

	/achievements
		POST: add new achievement
			[all values]

	/achievements?field=value
		GET: returns a list of matching achievements
			[any or no field(s)]

	/achievements/<id>
		GET: get a single achievement
		PUT: modify all values of achievement
			[all values, JWT]
		DELETE: delete a single achievement
			[JWT]


Academic Achievements [Resource]
	roll_no
	name
	batch : format [YYYY-YYYY]
	programme : enum ['B. Ed.', 'BBA (H) 4 years', 'BBA (General)', 'BBA (B&I)', 'BBA (T&TM)', 'BCA', 'B.Com (H)']
	category : enum ['goldmedalist', 'exemplary', 'both']

	/academics
		POST: add new achievement
			[all values, JWT]

	/academics?field=value
		GET (with optional url params): returns a list of matching achievements
			[any or no field(s)]

	/academics/<id>
		GET (with /<id>): get a single achievement
		PUT: Modify all values of achievement
			[all values, JWT]
		DELETE: delete a single achievement
			[JWT]


Teacher Achievements [Resource]
	ta_type : enum ['BOOK', 'JOURNAL', 'CONFERENCE', 'SEMINARATTENDED']
	sub_type : enum ['SEMINAR', 'CONFERENCE', 'WORKSHOP', 'FDP', 'FDP1WEEK']
	international : bool
	topic
	published
	sponsored : bool
	reviewed : bool
	date : format [YYYY-MM-DD]
	description
	msi : bool
	place

	/teacher_achievements
		POST: create new teacher achievement
			[all fields, JWT]

	/teacher_achievements?field=value
		GET (with optional url params): returns a list of matching achievements
			[any or no field(s)]

	/teacher_achievements/<id>
		GET: get achievements of a specific user
		PUT: update existing teacher achievement
			[all fields, JWT]
		DELETE: delete a single achievement of current user
			[JWT]

	/teacher_achievements/teachers [GET]
		GET: get a list of teachers who have achievements


Server status [Action]
	/
		GET: get server status


Authenticate user credentials [Action]
	/login
		POST: log in, get access token (JWT)
			[email, password]
```