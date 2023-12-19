class View:
	def __init__(self) -> None:
		pass

	def message(self, msg) -> None:
		print(f"{msg}", end="\n\n")

	def get_input(self, msg='') -> str:
		return input(msg).strip()
		
	def table(self, table, head=None) -> None:
		if head is not None:
			for elem in head:
				print(f"{elem}", sep=' ', end='')
			print()
		for row in table:
			for elem in row:
				print(f"{elem}", sep=' ', end='')
			print()