import psycopg2
import datetime as dt

generate_random_data_query = \
"""
with vars as (
	select
		%s as n,
		(select last_value from accounts_id_seq) as last_acc_id,
		(select last_value from journals_id_seq) as last_jrnl_id
),
accs as (
	select
		id,
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(48 + random() * 10)::int) ||
		chr(floor(48 + random() * 10)::int) ||
		chr(floor(48 + random() * 10)::int) ||
		'@example.mail' as email,
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) as password,
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(48 + random() * 10)::int) ||
		chr(floor(48 + random() * 10)::int) ||
		chr(floor(48 + random() * 10)::int) as name
	from generate_series(
		(select last_acc_id + 1 from vars),
		(select last_acc_id + n from vars)
	) as id
),
jrnls1 as (
	select
		id,
		chr(floor(65 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) as name,
		current_date - floor(random() * 365)::int as created_on,
		(select last_acc_id + 1 from vars) + floor(random() * (select n from vars))::bigint as account_id
	from generate_series(
		(select last_jrnl_id + 1 from vars),
		(select last_jrnl_id + n from vars)
	) as id
),
jrnls2 as (
	select j.*, j.created_on as last_edit
	from jrnls1 j
),
nots1 as (
	select
		row,
		chr(floor(65 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) as name,
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) ||
		chr(floor(97 + random() * 26)::int) as text,
		(select last_jrnl_id + 1 from vars) + floor(random() * (select n from vars))::bigint as journal_id
	from generate_series(
		1,
		(select n from vars)
	) as row
),
nots2 as (
	select
		n.*,
		j.created_on + floor(random() * (current_date - j.created_on))::int as added_on
	from nots1 n
	join jrnls2 j on j.id=n.journal_id
),
nots as (
	select
		n.*,
		case
			when random() > 0.5
			then 1
			else -1
		end * (random() * 30)::int + added_on
		as date
	from nots2 n
),
jrnls as (
	select j.id, j.name, j.created_on, f.last_edit, j.account_id
	from jrnls2 j
	join (
		select
			j2.id,
			case
				when max(n.added_on) is null
					then j2.last_edit
					else max(n.added_on)
			end as last_edit
		from jrnls2 j2
		left join nots n on j2.id=n.journal_id
		group by j2.id, j2.last_edit
	) as f on j.id=f.id
),
accs_insert as (
	insert into accounts (email, password, name)
	select email, password, name
	from accs
	order by id
),
jrnls_insert as (
	insert into journals (name, created_on, last_edit, account_id)
	select name, created_on, last_edit, account_id
	from jrnls
	order by id
),
nots_insert as (
	insert into notes (name, date, text, added_on, journal_id)
	select name, date, text, added_on, journal_id
	from nots
	order by row
)
select 1
"""

search1 = \
"""
select
	a.id as "account",
	a.email,
	j.id as "journal",
	j.name as "journal name",
	count(n.journal_id) as "notes in journal"
from accounts a
join journals j on a.id = j.account_id
join notes n on j.id = n.journal_id
where (j.created_on >= %s) and (j.created_on <= %s)
group by a.id, j.id, n.journal_id
order by a.id
"""

search2 = \
"""
select
	count(n.journal_id) as "notes count",
	j.id as "journal",
	j.created_on as "created on",
	j.name
from accounts a
join journals j on a.id=j.account_id
join notes n on j.id=n.journal_id
where (n.added_on >= %s) and (n.added_on <= %s)
group by j.id, j.created_on, n.journal_id
order by "notes count" desc, j.created_on
"""

search3 = \
"""
select
	a.id as "account",
	a.email,
	j.last_edit as "last edit on",
	j.id as "journal",
	n.id as "note",
	n.added_on as "added on"
from accounts a
join journals j on a.id=j.account_id
join notes n on j.id=n.journal_id
where (j.last_edit >= %s) and (j.last_edit <= %s)
group by a.id, j.id, n.id
order by j.last_edit, a.id
"""

class Model:
	def __init__(self) -> None:
		self.conn = psycopg2.connect(
			dbname="postgres",
			user="postgres",
			password="123457896_Qq",
			host="localhost",
			port=5432
			)

	def create_account(self, email, password, name) -> None:
		with self.conn.cursor() as cur:
			try:
				cur.execute('insert into accounts (email, password, name) values (%s, %s, %s)', (email, password, name))
				self.conn.commit()
			except psycopg2.errors.UniqueViolation as e:
				self.conn.rollback()
				raise e

	def edit_account(self, id, email, password, name) -> None:
		with self.conn.cursor() as cur:
			try:
				cur.execute('update accounts set email=%s, password=%s, name=%s where id=%s', (email, password, name, id))
				self.conn.commit()
			except psycopg2.errors.UniqueViolation as e:
				self.conn.rollback()
				raise e
		
	def delete_account(self, id):
		with self.conn.cursor() as cur:
			cur.execute('delete from accounts where id=%s', (id, ))
			self.conn.commit()

	def get_account(self, id):
		with self.conn.cursor() as cur:
			cur.execute('select * from accounts where id=%s', (id, ))
			return cur.fetchall()

	def get_all_accounts(self):
		with self.conn.cursor() as cur:
			cur.execute('select * from accounts')
			return cur.fetchall()


	def create_journal(self, name, account_id) -> None:
		with self.conn.cursor() as cur:
			try:
				created_on = dt.date.today()
				cur.execute('insert into journals (name, created_on, last_edit, account_id) values (%s, %s, %s, %s)', (name, created_on, created_on, account_id))
				self.conn.commit()
			except psycopg2.errors.UniqueViolation as e:
				self.conn.rollback()
				raise e

	def edit_journal(self, id, name, account_id) -> None:
		with self.conn.cursor() as cur:
			last_edit = dt.date.today()
			cur.execute('update journals set name=%s, account_id=%s, last_edit=%s where id=%s', (name, account_id, last_edit, id))
			self.conn.commit()
		
	def delete_journal(self, id):
		with self.conn.cursor() as cur:
			cur.execute('delete from journals where id=%s', (id, ))
			self.conn.commit()

	def get_journal(self, id):
		with self.conn.cursor() as cur:
			cur.execute('select * from journals where id=%s', (id, ))
			return cur.fetchall()

	def get_all_journals(self):
		with self.conn.cursor() as cur:
			cur.execute('select * from journals')
			return cur.fetchall()
		

	def create_note(self, name, date, text, journal_id) -> None:
		with self.conn.cursor() as cur:
			try:
				added_on = dt.date.today()
				cur.execute(
					'insert into notes (name, date, added_on, text, journal_id) values (%s, %s, %s, %s, %s);\n'
					'update journals set last_edit=%s where id=%s'
					, (name, date, added_on, text, journal_id, added_on, journal_id)
					)
				self.conn.commit()
			except psycopg2.errors.UniqueViolation as e:
				self.conn.rollback()
				raise e

	def edit_note(self, id, name, date, text, journal_id) -> None:
		with self.conn.cursor() as cur:
			edited_on = dt.date.today()
			cur.execute(
				'update notes set name=%s, date=%s, text=%s, journal_id=%s where id=%s;\n'
				'update journals set last_edit=%s where id=%s'
				, (name, date, text, journal_id, id, edited_on, journal_id)
				)
			self.conn.commit()
		
	def delete_note(self, id):
		with self.conn.cursor() as cur:
			cur.execute('select journal_id from notes where id=%s', (id, ))
			journal_id = cur.fetchall()[0][0]
			deleted_on = dt.date.today()
			cur.execute(
				'delete from notes where id=%s;\n'
				'update journals set last_edit=%s where id=%s'
				, (id, deleted_on, journal_id)
				)
			self.conn.commit()

	def get_note(self, id):
		with self.conn.cursor() as cur:
			cur.execute('select id, name, date, added_on, journal_id, text from notes where id=%s', (id, ))
			return cur.fetchall()

	def get_all_notes(self):
		with self.conn.cursor() as cur:
			cur.execute('select id, name, date, added_on, journal_id from notes')
			return cur.fetchall()
		

	def generate_random_data(self, rows):
		with self.conn.cursor() as cur:
			try:
				cur.execute(generate_random_data_query, (rows, ))
				self.conn.commit()
			except Exception as e:
				raise e
			
	
	def search1(self, left, right):
		with self.conn.cursor() as cur:
			cur.execute(search1, (left, right))
			return cur.fetchall()
		
	def search2(self, left, right):
		with self.conn.cursor() as cur:
			cur.execute(search2, (left, right))
			return cur.fetchall()
		
	def search3(self, left, right):
		with self.conn.cursor() as cur:
			cur.execute(search2, (left, right))
			return cur.fetchall()