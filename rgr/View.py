import datetime as dt

class View:
	def message(self, msg) -> None:
		print(f"{msg}", end="\n\n")

	def get_input(self, msg='') -> str:
		usr_input = input(msg).strip()
		print()
		return usr_input
		
	def table(self, table, head=None) -> None:
		lengths = None
		if head is not None:
			lengths = [len(elem) for elem in head]
		else:
			lengths = [len(elem) for elem in table[0]]

		for j in range(len(table[0])):
			for i in range(len(table)):
				lengths[j] = max(lengths[j], len(str(table[i][j])))

		if head is not None:
			print("| ", end='')
			for i, elem in enumerate(head):
				print(f"{elem:^{lengths[i]}} | ", end='')
			print()
		for row in table:
			print("| ", end='')
			for i, elem in enumerate(row):
				print(f"{str(elem):^{lengths[i]}} | ", end='')
			print()
		print()