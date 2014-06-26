import psycopg2, psycopg2.extras

class orm_db(object):
	def __init__(self):
		self._default_db = psycopg2.connect(dbname='postgres', user='postgres', password='123', connection_factory=psycopg2.extras.RealDictConnection)
		self.cursor = self._default_db.cursor()
	
	def commit(self):
		self._default_db.commit()
