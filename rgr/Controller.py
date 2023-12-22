from Model import *
from View import *
import time

class Controller:
	def __init__(self) -> None:
		self.model = Model()
		self.view = View()


	def run(self) -> None:
		options = {'1': self.accounts_sub, '2': self.journals_sub, '3': self.notes_sub, '4': self.generate_random_data, '5': self.search1, '6': self.search2, '7': self.search3}
		
		while True:
			self.view.message(
				"main menu\n"
				"1. accounts\n"
				"2. journals\n"
				"3. notes\n"
				"4. generate random data\n"
				"5. how many notes were created by account in journals, that were created in a date span\n"
				"6. how many notes, that were added in a date span, are in journals\n"
				"7. accounts, their journals that were lastly edited in a date span, and notes inside\n"
				"0. exit"
							  )
			
			option = self.view.get_input("option: ")

			if option == '0':
				return
			elif option in options:
				options[option]()
			else:
				self.view.message("please, input an integer in range 0-7")


	def accounts_sub(self) -> None:
		options = {'1': self.create_account, '2': self.edit_account, '3': self.delete_account, '4': self.show_account,'5': self.show_all_accounts}
		
		while True:
			self.view.message(
				"accounts\n"
				"1. create new\n"
				"2. edit existing\n"
				"3. delete existing\n"
				"4. show one\n"
				"5. show all\n"
				"0. go back"
							  )
			
			option = self.view.get_input("option: ")

			if option == '0':
				return
			elif option in options:
				options[option]()
			else:
				self.view.message("please, input an integer in range 0-5")

	def journals_sub(self) -> None:
		options = {'1': self.create_journal, '2': self.edit_journal, '3': self.delete_journal, '4': self.show_journal,'5': self.show_all_journals}
		
		while True:
			self.view.message(
				"journals\n"
				"1. create new\n"
				"2. edit existing\n"
				"3. delete existing\n"
				"4. show one\n"
				"5. show all\n"
				"0. go back"
							  )
			
			option = self.view.get_input("option: ")

			if option == '0':
				return
			elif option in options:
				options[option]()
			else:
				self.view.message("please, input an integer in range 0-5")

	def notes_sub(self) -> None:
		options = {'1': self.create_note, '2': self.edit_note, '3': self.delete_note, '4': self.show_note,'5': self.show_all_notes}
		
		while True:
			self.view.message(
				"notes\n"
				"1. create new\n"
				"2. edit existing\n"
				"3. delete existing\n"
				"4. show one\n"
				"5. show all\n"
				"0. go back"
							  )
			
			option = self.view.get_input("option: ")

			if option == '0':
				return
			elif option in options:
				options[option]()
			else:
				self.view.message("please, input an integer in range 0-5")


	def create_account(self):
		self.view.message(
			"specify new account details separated by comma: <email>, <password>, <name>\n"
			"input nothing to return back"
			)
		while True:
			details = self.view.get_input("details: ")

			try:
				if details == "":
					return
				email, password, name = [detail.strip() for detail in details.split(",")]
			except:
				self.view.message("please, input details in the right order and separate them with commas")
				continue

			if len(email) > 256 or len(password) > 128 or len(name) > 128:
				self.view.message("specified details are incorrect")
				continue

			try:
				self.model.create_account(email, password, name)
			except psycopg2.errors.UniqueViolation as e: 
				self.view.message("account with such email already exists")
				continue

			return

	def edit_account(self):
		id = None
		self.view.message(
			"specify id of the account you want to edit\n"
			"input nothing to return back"
			)
		
		while True:
			id = self.view.get_input("id: ")
			
			if id == "":
				return
			
			try:
				id = int(id)
				if len(self.model.get_account(id)) == 0:
					self.view.message("account with such id doesn't exist")
					continue
				break
			except:
				self.view.message("specified id is incorrect")
				continue

		self.view.message(
			"specify new account details separated by comma: <email>, <password>, <name>\n"
			"input nothing to return back"
			)
		while True:
			details = self.view.get_input("details: ")

			try:
				if details == "":
					return
				email, password, name = [detail.strip() for detail in details.split(",")]
			except:
				self.view.message("please, input details in the right order and separate them with commas")
				continue

			if len(email) > 256 or len(password) > 128 or len(name) > 128:
				self.view.message("specified details are incorrect")
				continue

			try:
				self.model.edit_account(id, email, password, name)
				return
			except psycopg2.errors.UniqueViolation as e:
				self.view.message("account with such email already exists")

	def delete_account(self):
		id = None
		self.view.message(
			"specify id of the account you want to delete\n"
			"input nothing to return back"
			)
		
		while True:
			id = self.view.get_input("id: ")
			
			if id == "":
				return
			
			try:
				id = int(id)
				if len(self.model.get_account(id)) == 0:
					self.view.message("account with such id doesn't exist")
					continue
			except:
				self.view.message("specified id is incorrect")
				continue

			acc = self.model.get_account(id)
			self.view.message(
				"are you sure you want to delete this account?\n"
				f"email: {acc[0][1]}\n"
				f"password: {acc[0][2]}\n"
				f"name: {acc[0][3]}"
				)
			while True:
				option = self.view.get_input("are you sure (y/n)? ").lower()

				if option == 'y':
					self.view.message("deleting account")
					self.model.delete_account(id)
					return
				elif option == 'n':
					self.view.message("specified account won't be deleted")
					break
					
	def show_account(self):
		id = None
		self.view.message(
			"specify id of the account you want to see\n"
			"input nothing to return back"
			)
		
		while True:
			id = self.view.get_input("id: ")
			
			if id == "":
				return
			
			try:
				id = int(id)
				if len(self.model.get_account(id)) == 0:
					self.view.message("account with such id doesn't exist")
					continue
				break
			except:
				self.view.message("specified id is incorrect")
				continue

		self.view.message("requested account")
		self.view.table(self.model.get_account(id), ["id", "email", "password", "name"])

	def show_all_accounts(self):
		self.view.message("all accounts")
		self.view.table(self.model.get_all_accounts(), ["id", "email", "password", "name"])


	def create_journal(self):
		self.view.message(
			"specify new journal details separated by comma: <name>, <account_id>\n"
			"input nothing to return back"
			)
		while True:
			details = self.view.get_input("details: ")

			try:
				if details == "":
					return
				name, account_id = [detail.strip() for detail in details.split(",")]
			except:
				self.view.message("please, input details in the right order and separate them with commas")
				continue

			try:
				account_id = int(account_id)
				if len(self.model.get_account(account_id)) == 0:
					self.view.message("account with such id doesn't exist")
					continue
			except:
				self.view.message(f"specified account id is incorrect")
				continue

			if len(name) > 128:
				self.view.message("specified name is incorrect")
				continue

			try:
				self.model.create_journal(name, account_id)
			except psycopg2.errors.UniqueViolation as e: 
				self.view.message("specified account already has a journal with such name")
				continue

			return

	def edit_journal(self):
		id = None
		self.view.message(
			"specify id of the journal you want to edit\n"
			"input nothing to return back"
			)
		
		while True:
			id = self.view.get_input("id: ")
			
			if id == "":
				return
			
			try:
				id = int(id)
				if len(self.model.get_journal(id)) == 0:
					self.view.message("journal with such id doesn't exist")
					continue
				break
			except:
				self.view.message("specified id is incorrect")
				continue

		self.view.message(
			"specify new journal details separated by comma: <name>, <account_id>\n"
			"input nothing to return back"
			)
		while True:
			details = self.view.get_input("details: ")

			try:
				if details == "":
					return
				name, account_id = [detail.strip() for detail in details.split(",")]
			except:
				self.view.message("please, input details in the right order and separate them with commas")
				continue

			try:
				account_id = int(account_id)
				if len(self.model.get_account(account_id)) == 0:
					self.view.message("account with such id doesn't exist")
					continue
			except:
				self.view.message("specified account id is incorrect")
				continue

			if len(name) > 128:
				self.view.message("specified name is incorrect")
				continue

			try:
				self.model.edit_journal(id, name, account_id)
			except psycopg2.errors.UniqueViolation as e: 
				self.view.message("specified account already has a journal with such name")
				continue

			return

	def delete_journal(self):
		id = None
		self.view.message(
			"specify id of the journal you want to delete\n"
			"input nothing to return back"
			)
		
		while True:
			id = self.view.get_input("id: ")
			
			if id == "":
				return
			
			try:
				id = int(id)
				if len(self.model.get_journal(id)) == 0:
					self.view.message("journal with such id doesn't exist")
					continue
			except:
				self.view.message("specified id is incorrect")
				continue

			jrnl = self.model.get_journal(id)
			self.view.message(
				"are you sure you want to delete this journal?\n"
				f"name: {jrnl[0][1]}\n"
				f"account id: {jrnl[0][4]}\n"
				f"created_on: {jrnl[0][2]}\n"
				f"last_edit: {jrnl[0][3]}"
				)
			while True:
				option = self.view.get_input("are you sure (y/n)? ").lower()

				if option == 'y':
					self.view.message("deleting journal")
					self.model.delete_journal(id)
					return
				elif option == 'n':
					self.view.message("specified journal won't be deleted")
					break
					
	def show_journal(self):
		id = None
		self.view.message(
			"specify id of the journal you want to see\n"
			"input nothing to return back"
			)
		
		while True:
			id = self.view.get_input("id: ")
			
			if id == "":
				return
			
			try:
				id = int(id)
				if len(self.model.get_journal(id)) == 0:
					self.view.message("journal with such id doesn't exist")
					continue
				break
			except:
				self.view.message("specified id is incorrect")
				continue

		self.view.message("requested journal")
		self.view.table(self.model.get_journal(id), ["id", "name", "created on", "last edit", "account id"])

	def show_all_journals(self):
		self.view.message("all journals")
		self.view.table(self.model.get_all_journals(), ["id", "name", "created on", "last edit", "account id"])


	def create_note(self):
		self.view.message(
			"specify new note details separated by comma: <name>, <date>, <journal_id>\n"
			"input date in next format <year>-<month>-<day>\n"
			"input nothing to return back"
			)
		while True:
			details = self.view.get_input("details: ")

			if details == "":
				return
			
			try:	
				name, date, journal_id = [detail.strip() for detail in details.split(",")]
			except:
				self.view.message("please, input details in the right order and separate them with commas")
				continue

			try:
				journal_id = int(journal_id)
				if len(self.model.get_journal(journal_id)) == 0:
					self.view.message("journal with such id doesn't exist")
					continue
			except:
				self.view.message(f"specified journal id is incorrect")
				continue

			if len(name) > 128:
				self.view.message("specified name is incorrect")
				continue

			try:
				date = dt.datetime.strptime(date, "%Y-%m-%d")
			except:
				self.view.message("specified date is incorrect")
				continue

			self.view.message(
				"enter note's text (multiline text is not supported)\n"
				"input nothing to return back"
				)
			text = None
			while True:
				text = self.view.get_input("text: ")

				if text == "":
					break

				self.view.message(f"is this your desired text?\n{text}")

				while True:
					option = self.view.get_input("are you sure (y/n)? ")

					if option == 'y':
						self.model.create_note(name, date, text, journal_id)
						return
					elif option == 'n':
						break

	def edit_note(self):
		id = None
		self.view.message(
			"specify id of the note you want to edit\n"
			"input nothing to return back"
			)
		
		while True:
			id = self.view.get_input("id: ")
			
			if id == "":
				return
			
			try:
				id = int(id)
				if len(self.model.get_note(id)) == 0:
					self.view.message("note with such id doesn't exist")
					continue
				break
			except:
				self.view.message("specified id is incorrect")
				continue

		self.view.message(
			"specify new note details separated by comma: <name>, <date>, <journal_id>\n"
			"input nothing to return back"
			)
		while True:
			details = self.view.get_input("details: ")

			if details == "":
				return
			
			try:
				name, date, journal_id = [detail.strip() for detail in details.split(",")]
			except:
				self.view.message("please, input details in the right order and separate them with commas")
				continue

			try:
				journal_id = int(journal_id)
				if len(self.model.get_journal(journal_id)) == 0:
					self.view.message("journal with such id doesn't exist")
					continue
			except:
				self.view.message(f"specified journal id is incorrect")
				continue

			if len(name) > 128:
				self.view.message("specified name is incorrect")
				continue

			try:
				date = dt.datetime.strptime(date, "%Y-%m-%d")
			except:
				self.view.message("specified date is incorrect")
				continue

			self.view.message(
				"enter note's text (multiline text is not supported)\n"
				"input nothing to return back"
				)
			text = None
			while True:
				text = self.view.get_input()

				if text == "":
					break

				self.view.message(f"is this your desired text?\n{text}")

				while True:
					option = self.view.get_input("are you sure (y/n)? ")

					if option == 'y':
						self.model.edit_note(id, name, date, text, journal_id)
						return
					elif option == 'n':
						break

	def delete_note(self):
		id = None
		self.view.message(
			"specify id of the note you want to delete\n"
			"input nothing to return back"
			)
		
		while True:
			id = self.view.get_input("id: ")
			
			if id == "":
				return
			
			try:
				id = int(id)
				if len(self.model.get_note(id)) == 0:
					self.view.message("note with such id doesn't exist")
					continue
			except:
				self.view.message("specified id is incorrect")
				continue

			note = self.model.get_note(id)
			self.view.message(
				"are you sure you want to delete this note?\n"
				f"name: {note[0][1]}\n"
				f"date: {note[0][2]}\n"
				f"added on: {note[0][3]}\n"
				f"journal id: {note[0][4]}\n"
				f"text:\n{note[0][5]}"
				)
			while True:
				option = self.view.get_input("are you sure (y/n)? ").lower()

				if option == 'y':
					self.view.message("deleting note")
					self.model.delete_note(id)
					return
				elif option == 'n':
					self.view.message("specified note won't be deleted")
					break
					
	def show_note(self):
		id = None
		self.view.message(
			"specify id of the note you want to see\n"
			"input nothing to return back"
			)
		
		while True:
			id = self.view.get_input("id: ")
			
			if id == "":
				return
			
			try:
				id = int(id)
				if len(self.model.get_note(id)) == 0:
					self.view.message("note with such id doesn't exist")
					continue
				break
			except:
				self.view.message("specified id is incorrect")
				continue

		self.view.message("requested note")
		self.view.table(self.model.get_note(id), ["id", "name", "date", "added_on", "journal id", "text"])

	def show_all_notes(self):
		notes = self.model.get_all_notes()
		if len(notes) != 0:
			self.view.message("all notes")
			self.view.table(notes, ["id", "name", "date", "added on", "journal id"])
		else:
			self.view.message("there are no notes")


	def generate_random_data(self):
		self.view.message(
			"specify how many rows of random data in every table you want\n"
			"input nothing to return back"
			)
		rows = None
		while True:
			rows = self.view.get_input("rows: ")

			if rows == "":
				return
			
			try:
				rows = int(rows)
				if rows < 1:
					self.view.message("specified rows number is incorrect")
					continue
				break
			except:
				self.view.message("specified rows number is incorrect")
				continue

		self.view.message("generating data...")
		start, end = time.time_ns(), 0
		try:
			self.model.generate_random_data(rows)
		except:
			self.view.message("something went wrong, data is not generated")
			return
		end = time.time_ns()
		self.view.message(f"data was generated in {(end - start) / 10**6} ms")


	def search1(self):
		self.view.message(
			"specify date span when the journals were created: <date>, <date>\n"
			"input date in next format <year>-<month>-<day>\n"
			"input nothing to return back"
			)
		while True:
			details = self.view.get_input("details: ")

			if details == "":
				return
			
			try:	
				left, right = [detail.strip() for detail in details.split(",")]
			except:
				self.view.message("please, input details in the right order and separate them with commas")
				continue

			try:
				left = dt.datetime.strptime(left, "%Y-%m-%d")
			except:
				self.view.message("specified left date is incorrect")
				continue

			try:
				right = dt.datetime.strptime(right, "%Y-%m-%d")
			except:
				self.view.message("specified right date is incorrect")
				continue

			if left > right:
				self.view.message("left date must be less or equal to right")
				continue
			break

		start, end = time.time_ns(), 0
		table = self.model.search1(left, right)
		end = time.time_ns()
		self.view.table(table, ["account", "email", "journal", "journal name", "notes in journal"])
		self.view.message(f"data was searched up in {(end - start) / 10**6} ms")

	def search2(self):
		self.view.message(
			"specify date span when the notes were added: <date>, <date>\n"
			"input date in next format <year>-<month>-<day>\n"
			"input nothing to return back"
			)
		while True:
			details = self.view.get_input("details: ")

			if details == "":
				return
			
			try:	
				left, right = [detail.strip() for detail in details.split(",")]
			except:
				self.view.message("please, input details in the right order and separate them with commas")
				continue

			try:
				left = dt.datetime.strptime(left, "%Y-%m-%d")
			except:
				self.view.message("specified left date is incorrect")
				continue

			try:
				right = dt.datetime.strptime(right, "%Y-%m-%d")
			except:
				self.view.message("specified right date is incorrect")
				continue

			if left > right:
				self.view.message("left date must be less or equal to right")
				continue
			break

		start, end = time.time_ns(), 0
		table = self.model.search2(left, right)
		end = time.time_ns()
		self.view.table(table, ["notes count", "journal", "created on", "name"])
		self.view.message(f"data was searched up in {(end - start) / 10**6} ms")

	def search3(self):
		self.view.message(
			"specify date span when the journals were last edited: <date>, <date>\n"
			"input date in next format <year>-<month>-<day>\n"
			"input nothing to return back"
			)
		while True:
			details = self.view.get_input("details: ")

			if details == "":
				return
			
			try:	
				left, right = [detail.strip() for detail in details.split(",")]
			except:
				self.view.message("please, input details in the right order and separate them with commas")
				continue

			try:
				left = dt.datetime.strptime(left, "%Y-%m-%d")
			except:
				self.view.message("specified left date is incorrect")
				continue

			try:
				right = dt.datetime.strptime(right, "%Y-%m-%d")
			except:
				self.view.message("specified right date is incorrect")
				continue

			if left > right:
				self.view.message("left date must be less or equal to right")
				continue
			break

		start, end = time.time_ns(), 0
		table = self.model.search3(left, right)
		end = time.time_ns()
		self.view.table(table, ["account", "email", "last edit on", "journal", "note", "added on"])
		self.view.message(f"data was searched up in {(end - start) / 10**6} ms")