import time
import psycopg2

class Model:
	def __init__(self) -> None:
		self.conn = psycopg2.connect(
			dbname="journals",
			user="postgres",
			password="123",
			host="localhost",
			port=5432
			)

	def create_account(self, email, password, name) -> None:
		with self.conn.cursor() as cur:
			cur.execute('insert into accounts (email, password, name) values (%s, %s, %s)', (email, password, name))
			self.conn.commit()

	def edit_account(self, id, email, password, name) -> None:
		pass
	
	def delete_client(self, id):
		pass

	def get_client(self, id):
		pass
	
	def get_all_clients(self):
		pass