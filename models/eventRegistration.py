# from models.model import db

# class EventRegistration(db.Model):

# 	__tablename__ = 'EventRegistration'

# 	eventId = db.Column(db.String(255), nullable=False, db.ForeignKey('event.eventId'))
# 	teamId = db.Column(db.String(255), nullable=False)
# 	leaderId = db.Column(db.String(255), nullable=False, db.ForeignKey('user.userName'))

# 	def as_dict(self):
# 		return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}


