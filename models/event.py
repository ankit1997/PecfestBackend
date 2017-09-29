from models.model import db

class Event(db.Model):

	__tablename__ = 'Event'

	eventId = db.Column(db.Integer, primary_key=True, nullable=False)
	eventName = db.Column(db.String(100), unique=True, nullable=False)
	headId = db.Column(db.String(100))
	location = db.Column(db.String(200))
	day = db.Column(db.Integer)
	time = db.Column(db.String(50))
	prize = db.Column(db.String(50))
	minSize = db.Column(db.Integer, default=0)
	maxSize = db.Column(db.Integer, default=0)

	eventType = db.Column(db.Integer, nullable=False)
	eventCategory = db.Column(db.Integer, default=0)
	clubId = db.Column(db.Integer, default=0)
	eventDetails = db.Column(db.String(300))
	eventDetailsWeb = db.Column(db.String(300))

	imageUrl = db.Column(db.String(255), default='')
	instructions = db.Column(db.String(300))
	instructionsWeb = db.Column(db.String(300), nullable=False)

	lecture = db.Column(db.Integer, nullable=False, default=0)
	pdfUrl = db.Column(db.String(255), nullable=False)

	# registration = db.relationship('Registration', backref='event', lazy=True)

	# def __init__(self):
	# 	pass

	# def __init__(self, eventName, headId='', location, day=0, time, prize, minSize=0, maxSize=0, 
	# 					eventType, eventCategory=0, clubId=0, eventDetails, eventDetailsWeb, imageUrl='', instructions, 
	# 					instructionsWeb, lecture=0, pdfUrl):
	# 	self.eventName = eventName
	# 	self.headId = headId
	# 	self.location = location
	# 	self.day = day
	# 	self.time = time
	# 	self.prize = prize
	# 	self.minSize = minSize
	# 	self.maxSize = maxSize
	# 	self.eventType = eventType
	# 	self.eventCategory = eventCategory
	# 	self.clubId = clubId
	# 	self.eventDetails = eventDetails
	# 	self.eventDetailsWeb = eventDetailsWeb
	# 	self.imageUrl = imageUrl
	# 	self.instructions = instructions
	# 	self.instructionsWeb = instructionsWeb
	# 	self.lecture = lecture
	# 	self.pdfUrl = pdfUrl

	def __repr__(self):
		return 'Event: <' + self.eventName + '>'

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}


