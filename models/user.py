from models.model import db

class User(db.Model):
	'''
		Contain details of a user.
	'''

	__tablename__ = 'User'

  	pecfestId = db.Column(db.String(6), primary_key=True)
	name = db.Column(db.String(256), nullable=False)
	college = db.Column(db.String(256), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	mobile = db.Column(db.String(10), nullable=False)
	gender = db.Column(db.String(1), nullable=False)
	accomodation = db.Column(db.String(255), nullable=False)
	verified = db.Column(db.Integer, nullable=False)
	smsCounter = db.Column(db.Integer, default=0)
	
	registration = db.relationship('Registration', backref='user', lazy=True)

	def __repr__(self):
		return 'User: <' + self.pecfestId + ':' + name + '>'

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}


