from Model import *
from View import *

class Controller:
	def __init__(self) -> None:
		self.model = Model()
		self.view = View()


	def run(self) -> None:
		options = {'1': self.accounts_sub, '2': self.journals_sub, '3': self.notes_sub}
		
		while True:
			self.view.message(
				"main menu\n"
				"1. accounts\n"
				"2. journals\n"
				"3. notes\n"
				"0. exit"
							  )
			
			option = self.view.get_input()

			if option == '0':
				return
			elif option in options:
				options[option]()
			else:
				self.view.message("please, input an integer in range 0-3")


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
		options = {'1': self.view.create_journal, '2': self.view.edit_journal, '3': self.view.delete_journal, '4': self.show_journal,'5': self.show_all_journals}
		
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
		options = {'1': self.view.create_note, '2': self.view.edit_note, '3': self.view.delete_note, '4': self.show_note,'5': self.show_all_notes}
		
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

			self.model.create_account(email, password, name)
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
				break
			except:
				self.view.message("specified id is incorrect")

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

			self.model.edit_account(id, email, password, name)
			return

	def delete_account(self):
		arguments = self.view.delete_client()
		id = arguments.strip()
		try:
			id = int(id)
			if len(self.model.get_client(id)) == 0:
				self.view.warn("ID doesn't exist")
				return
		except:
			self.view.warn(f"Bad ID")
			return
		self.model.delete_client(id)

	def show_account(self):
		self.view.show_clients(self.model.get_all_clients())

	def show_all_accounts(self):
		self.view.show_clients(self.model.get_all_clients())