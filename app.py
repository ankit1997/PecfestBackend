from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

################################################################

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/pecfestdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

################################################################

from models.model import pass_param

pass_param(db)

from models.event import Event
from models.user import User
from models.pecfestIds import PecfestIds

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

	eventName = data["eventName"]
	headId = data["headId"]
	location = data["location"]
	day = data["day"]
	time = data["time"]
	prize = data["prize"]
	minSize = data["minSize"]
	maxSize = data["maxSize"]
	eventType = data["eventType"]
	eventCategory = data["eventCategory"]
	clubId = data["clubId"]
	eventDetails = data["eventDetails"]
	eventDetailsWeb = data["eventDetailsWeb"]
	imageUrl = data["imageUrl"]
	instructions = data["instructions"]
	instructionsWeb = data["instructionsWeb"]
	lecture = data["lecture"]
	pdfUrl = data["pdfUrl"]

	event =  Event(eventName=eventName, 
					headId=headId,
					location=location, 
					day=day, 
					time=time, 
					prize=prize, 
					minSize=minSize,
					maxSize=maxSize,
					eventType=eventType, 
					eventCategory=eventCategory,
					clubId=clubId,
					eventDetails=eventDetails, 
					eventDetailsWeb=eventDetailsWeb, 
					imageUrl=imageUrl,
					instructions=instructions, 
					instructionsWeb=instructionsWeb, 
					lecture=lecture,
					pdfUrl=pdfUrl)

	curr_session = db.session
	success = False
	try:
		curr_session.add(event)
		curr_session.commit()
		success = True
	except:
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
	eventInfo["eventId"] = event.eventId
	eventInfo["eventName"] = event.eventName
	eventInfo["headId"] = event.headId
	eventInfo["location"] = event.location
	eventInfo["day"] = event.day
	eventInfo["time"] = event.time
	eventInfo["prize"] = event.prize
	eventInfo["minSize"] = event.minSize
	eventInfo["maxSize"] = event.maxSize
	eventInfo["eventType"] = event.eventType
	eventInfo["eventCategory"] = event.eventCategory
	eventInfo["clubId"] = event.clubId
	eventInfo["eventDetails"] = event.eventDetails
	eventInfo["eventDetailsWeb"] = event.eventDetailsWeb
	eventInfo["imageUrl"] = event.imageUrl
	eventInfo["instructions"] = event.instructions
	eventInfo["instructionsWeb"] = event.instructionsWeb
	eventInfo["lecture"] = event.lecture
	eventInfo["pdfUrl"] = event.pdfUrl

	return jsonify(eventInfo)


# Get event details
@app.route('/event/category/<int:eventCategory>', methods=['GET'])
def getEventFromCategory(eventId):

	eventsInfo = {}
	events = Event.query.filter_by(eventCategory=eventCategory)

	if events == None:
		eventsInfo["ACK"] = "FAILED"
		return jsonify(eventsInfo)

	eventsInfo["ACK"] = "SUCCESS"

	for event in events:
		eventInfo = {}
		eventInfo["eventId"] = event.eventId
		eventInfo["eventName"] = event.eventName
		eventInfo["headId"] = event.headId
		eventInfo["location"] = event.location
		eventInfo["day"] = event.day
		eventInfo["time"] = event.time
		eventInfo["prize"] = event.prize
		eventInfo["minSize"] = event.minSize
		eventInfo["maxSize"] = event.maxSize
		eventInfo["eventType"] = event.eventType
		eventInfo["eventCategory"] = event.eventCategory
		eventInfo["clubId"] = event.clubId
		eventInfo["eventDetails"] = event.eventDetails
		eventInfo["eventDetailsWeb"] = event.eventDetailsWeb
		eventInfo["imageUrl"] = event.imageUrl
		eventInfo["instructions"] = event.instructions
		eventInfo["instructionsWeb"] = event.instructionsWeb
		eventInfo["lecture"] = event.lecture
		eventInfo["pdfUrl"] = event.pdfUrl

		eventsInfo[event.eventName] = eventInfo

	return jsonify(eventsInfo)

################################################################
#####################USER INFO##################################

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
	accomodation = data['accomodation']
	verified = data['verified']
	smsCounter = 0

	alreadyUser = User.query.filter_by(email=email).first()
	if alreadyUser:
		return jsonify({'ACK': 'ALREADY'})

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

	curr_session = db.session
	success = False
	try:
		curr_session.add(user)
		curr_session.add(newPecfestId)
		curr_session.commit()
		success = True
	except:
		curr_session.rollback()
		curr_session.flush()

	if success:
		return jsonify({'ACK': 'SUCCESS'})
	return jsonify({'ACK': 'FAILED'})

# Get user's details
@app.route('/user/<string:userName>', methods=['GET'])
def getUserDetails(userName):
	userInfo = {}
	user = User.query.filter_by(userName=userName).first()

	if user == None:
		userInfo["ACK"] = "FAILED"
		return jsonify(userInfo)

	userInfo["ACK"] = "SUCCESS"
	userInfo["userName"] = user.userName
	userInfo["name"] = user.name
	userInfo["gender"] = user.gender
	userInfo["email"] = user.email
	userInfo["mobile"] = user.mobile
	userInfo["probNum"] = user.probNum
	userInfo["profileImg"] = user.profileImg

	return jsonify(userInfo)

################################################################
#####################REGISTRATION###############################



################################################################


################################################################

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=10001)

