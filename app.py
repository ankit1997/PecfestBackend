import string
from flask import Flask, request, jsonify
import random
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from requests import post

eventTypes = { 'Technical': 1, 'Cultural': 2, 'Lectures': 3, 'Workshops': 4, 'Shows': 5 }
categories = {
	"NATYAMANCH": 1,
	"NRITYAMANCH": 2,
	"LITERARY ARTS": 3,
	"SPEAKING ARTS": 4,
	"DIGITAL DESIGN ART": 5,
	"FINE ARTS": 6,
	"MUSICAL ARTS": 7,
	"ENTREPRENEURICAL ARTS": 8,
}

################################################################

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/pecfestdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

################################################################

from models.model import pass_param

pass_param(db)

from models.event import Event
from models.user import User
from models.pecfestIds import PecfestIds
from models.otps import OTPs
from models.event_registration import EventRegistration
from models.sent_sms import SentSMS

################################################################

def genPecfestId(name, length=6):
	done=False
	proposedId = ''
	while not done:
		proposedId = name + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
		alreadyId = PecfestIds.query.filter_by(pecfestId=proposedId).first()
		if alreadyId == None:
			break
	return proposedId


db.create_all()

################################################################
#####################EVENT MANAGEMENT###########################

# Create event
@app.route('/event/create', methods=['POST'])
def createEvent():
	data = request.get_json()

	name = data["name"]
	coordinators = data["coordinators"]
	location = data["location"] if "location" in data else ''
	day = data["day"] if "day" in data else 0
	time = data["time"] if "time" in data else "0"
	prize = data["prize"] if "prize" in data else "0"
	minSize = data["minSize"] if "minSize" in data else 1
	maxSize = data["maxSize"] if "maxSize" in data else 1
	eventType = eventTypes[data["eventType"]]
	category = categories[data["category"]]
	clubId = data["clubId"] if "clubId" in data else "PEC"
	details = data["details"] if "details" in data else ""
	shortDescription = data["shortDescription"] if "shortDescription" in data else ""
	imageUrl = data["imageUrl"] if "imageUrl" in data else ""
	rulesList = data["rulesList"] if "rulesList" in data else ""
	pdfUrl = data["pdfUrl"] if "pdfUrl" in data else ""

	event =  Event(name=name,
					coordinators=coordinators,
					location=location,
					day=day,
					time=time,
					prize=prize,
					minSize=minSize,
					maxSize=maxSize,
					eventType=eventType,
					category=category,
					clubId=clubId,
					details=details,
					shortDescription=shortDescription,
					imageUrl=imageUrl,
					rulesList=rulesList,
					pdfUrl=pdfUrl)

	curr_session = db.session
	success = False
	try:
		curr_session.add(event)
		curr_session.commit()
		success = True
	except Exception as err:
		print(err);
		curr_session.rollback()
		curr_session.flush()


	if success:
		return jsonify({'ACK': 'SUCCESS'})
	return jsonify({'ACK': 'FAILED'})

# Get event details
@app.route('/event/<int:eventId>', methods=['GET'])
def getEventDetails(eventId):

	eventInfo = {}
	event = Event.query.filter_by(eventId=eventId).first()

	if event == None:
		eventInfo["ACK"] = "FAILED"
		return jsonify(eventInfo)

	eventInfo["ACK"] = "SUCCESS"
	eventInfo["id"] = event.eventId
	eventInfo["name"] = event.name
	eventInfo["coordinators"] = event.coordinators
	eventInfo["location"] = event.location
	eventInfo["day"] = event.day
	eventInfo["time"] = event.time
	eventInfo["prize"] = event.prize
	eventInfo["minSize"] = event.minSize
	eventInfo["maxSize"] = event.maxSize
	eventInfo["eventType"] = event.eventType
	eventInfo["category"] = event.category
	eventInfo["clubId"] = event.clubId
	eventInfo["details"] = event.details
	eventInfo["shortDescription"] = event.shortDescription
	eventInfo["imageUrl"] = event.imageUrl
	eventInfo["rulesList"] = event.rulesList
	eventInfo["pdfUrl"] = event.pdfUrl

	return jsonify(eventInfo)


# Get event details
@app.route('/event/category/<int:eventCategory>', methods=['GET'])
def getEventFromCategory(eventCategory):

	eventsInfo = {}
	events = Event.query.filter_by(category=eventCategory)

	if events == None:
		eventsInfo["ACK"] = "FAILED"
		return jsonify(eventsInfo)

	eventsInfo["ACK"] = "SUCCESS"

	for event in events:
		eventInfo = {}

		eventInfo["id"] = event.eventId
		eventInfo["name"] = event.name
		eventInfo["coordinators"] = event.coordinators
		eventInfo["location"] = event.location
		eventInfo["day"] = event.day
		eventInfo["time"] = event.time
		eventInfo["prize"] = event.prize
		eventInfo["minSize"] = event.minSize
		eventInfo["maxSize"] = event.maxSize
		eventInfo["eventType"] = event.eventType
		eventInfo["category"] = event.category
		eventInfo["clubId"] = event.clubId
		eventInfo["details"] = event.details
		eventInfo["shortDescription"] = event.shortDescription
		eventInfo["imageUrl"] = event.imageUrl
		eventInfo["rulesList"] = event.rulesList
		eventInfo["pdfUrl"] = event.pdfUrl

		eventsInfo[event.name] = eventInfo

	return jsonify(eventsInfo)

################################################################
#####################USER INFO##################################

def sendOTP(name, mobile, otp):
	data = dict()

	data['user'] = 'onlineteam.pecfest'
	data['password'] = 'onlinesms'
	data['sid'] = 'PECCHD'
	data['msisdn'] = '91' + mobile
	name = name.split(' ')[0]
	data['msg'] = "Hi " + name + "! Welcome to PECFEST, 2017. Your OTP is " + otp + ". Enter this OTP into the website/app to get your PECFEST ID. Happy participating!"
	data['gwid'] = 2
	data['fl'] = 0
	headers = { 'Content-Type': 'application/x-www-form-urlencoded' }

	res = post('http://www.smslane.com//vendorsms/pushsms.aspx', data=data, headers=headers)
	if res.status_code is not 200:
		return False
	else:
		text = res.text
		if 'Message Id' in text:
			messageId = text.split(' : ')
			sms = SentSMS(smsId=messageId, mobile=mobile, smsType=1, status=1)

			session = db.session
			success = False
			try:
				session.add(sms)
				session.commit()
				success = True
			except:
				session.rollback()
				session.flush()
			return True
		else:
			print(text)
			return False



# Create User
@app.route('/user/create', methods=['POST'])
def createUser():
	data = request.get_json()

	name = data['name']
	pecfestId = genPecfestId(name[:3].strip().upper())
	college = data['college']
	email = data['email']
	mobile = data['mobile']
	gender = data['gender']
	accomodation = data['accomodation'] if "accomodation" in data else ""
	verified = 0
	smsCounter = 0


	alreadyUser = User.query.filter_by(mobile=mobile).first()
	if alreadyUser:
		return jsonify({'ACK': 'ALREADY', 'message': 'Phone number already registered.' })

	user = User(pecfestId=pecfestId,
				name=name,
				college=college,
				email=email,
				mobile=mobile,
				gender=gender,
				accomodation=accomodation,
				verified=verified,
				smsCounter=smsCounter)

	newPecfestId = PecfestIds(pecfestId=pecfestId)

	OTP = ''.join(random.choice(string.digits) for _ in range(6))
	otp = OTPs(mobile=mobile,
				otp=OTP)

	# send otp to the user's mobile number
	status = sendOTP(name, mobile, OTP)
	if not status:
		return jsonify({ 'ACK': 'FAILED', 'message': 'Unable to send OTP.' })

	curr_session = db.session
	success = False
	try:
		curr_session.add(user)
		curr_session.add(newPecfestId)
		curr_session.add(otp)
		curr_session.commit()
		success = True
	except Exception as err:
		print(err)
		curr_session.rollback()
		curr_session.flush()

	if success:
		return jsonify({'ACK': 'SUCCESS'})
	return jsonify({'ACK': 'FAILED'})

# Get user's details
@app.route('/user/<string:pecfestId>', methods=['GET'])
def getUserDetails(pecfestId):
	userInfo = {}
	user = User.query.filter_by(pecfestId=pecfestId).first()

	if user == None:
		userInfo["ACK"] = "FAILED"
		return jsonify(userInfo)

	userInfo["ACK"] = "SUCCESS"
	userInfo["pecfestId"] = user.pecfestId
	userInfo["name"] = user.name
	userInfo["college"] = user.college
	userInfo["gender"] = user.gender

	return jsonify(userInfo)


# verify user
@app.route('/user/verify', methods=['POST'])
def verifyUser():
	userInfo = {}
	json = request.get_json()
	o = json['otp']
	mobile = json['mobile']

	otp = OTPs.query.filter_by(mobile=mobile,
								otp=o).first()

	print(otp)

	if otp:
		curr_session = db.session
		user = User.query.filter_by(mobile=mobile).update(dict(verified=1))
		user = User.query.filter_by(mobile=mobile).first()

		if user:
			success = False
			try:
				curr_session.delete(otp)
				curr_session.commit()
				success = True
			except:
				curr_session.rollback()
				curr_session.flush()


			if success:
				userInfo['ACK'] = 'SUCCESS'
				userInfo["pecfestId"] = user.pecfestId
				userInfo["name"] = user.name
				userInfo["college"] = user.college
				userInfo["gender"] = user.gender

				return jsonify(userInfo)
			else:
				return jsonify({'ACK': 'FAILED' })
		else:
			return jsonify({ 'ACK': 'FAILED' })
	else:
		return jsonify({'ACK': 'FAILED', 'message': 'Wrong OTP'})


################################################################
#####################REGISTRATION###############################

@app.route('/event/register', methods=['POST'])
def registerEvent():
	try:
		json = request.get_json()

		eventId = json['eventId']
		event = Event.query.filter_by(eventId=eventId).first()

		team = [ member for member in json['team'] ]
		teamLeaderId = json['leader']

		if teamLeaderId not in team:
			return jsonify({ 'ACK': 'FAILED', 'message': 'Leader not from team' })

		for pecfestId in team:
			user = User.query.filter_by(pecfestId=pecfestId).first()
			if not user:
				return jsonify({ 'ACK': 'FAILED', 'message': 'Invalid members' })

		## check whether users are already registered or not
		for pecfestId in team:
			reg = EventRegistration.query.filter_by(memberId=pecfestId, eventId=eventId).first()
			if reg:
				return jsonify({ 'ACK': 'FAILED', 'message': pecfestId + ' is already registered to this event.'})

		## register this team in the database
		regs = []
		for pecfestId in team:
			reg = EventRegistration(
							eventId=eventId,
							memberId=pecfestId,
							leaderId=teamLeaderId)
			regs.append(reg)

		session = db.session
		success = False
		try:
			for reg in regs:
				session.add(reg)

			session.commit()
			success = True
		except Exception as err:
			session.rollback()
			session.flush()

		if success:
			return jsonify({ 'ACK': 'SUCCESS' })
		else:
			return jsonify({ 'ACK': 'FAILED' })
	except:
		return jsonify({ 'ACK': 'FAILED' })


################################################################


################################################################

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=10001)

