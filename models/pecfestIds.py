from models.model import db

class PecfestIds(db.Model):

	__tablename__ = 'PecfestIds'

  	pecfestId = db.Column(db.String(6), primary_key=True)

	def __repr__(self):
		return 'ID: <' + self.eventName + '>'

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}


