# from models.model import db

# class Registration(db.Model):

# 	__tablename__ = 'Registration'

# 	counter = db.Column(db.Integer, nullable=False)
# 	name = db.Column(db.String(255), nullable=False)
# 	college = db.Column(db.String(255), nullable=False)
# 	email = db.Column(db.String(255), nullable=False)
# 	phone = db.Column(db.String(255), nullable=False)
# 	gender = db.Column(db.String(1), nullable=False)
# 	accomodation = db.Column(db.String(255), nullable=False)
# 	pecfestId = db.Column(db.String(255), nullable=False)
# 	verified = db.Column(db.Integer, nullable=False)
# 	website = db.Column(db.Integer, nullable=False)
# 	smsCounter = db.Column(db.Integer, default=0)

# 	def as_dict(self):
# 		return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}


