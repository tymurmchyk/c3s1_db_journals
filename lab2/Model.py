import psycopg2
import datetime as dt
from typing import List
from sqlalchemy import ForeignKey, Text, String, BigInteger, Date, Time, Sequence
from sqlalchemy import create_engine
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session


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

class Base(DeclarativeBase):
	pass

class Account(Base):
	__tablename__ = "accounts"

	id: Mapped[int] = mapped_column(BigInteger, Sequence('accounts_id_seq'), primary_key=True)
	email: Mapped[str] = mapped_column(String(256))
	password: Mapped[str] = mapped_column(String(128))
	name: Mapped[str] = mapped_column(String(128))

	journals: Mapped['Journal'] = relationship(back_populates="account")

	def __repr__(self):
		return f"account : {self.id}, {self.email}, {self.password}, {self.name}"

class Journal(Base):
	__tablename__ = "journals"

	id: Mapped[int] = mapped_column(BigInteger, Sequence('journals_id_seq'), primary_key=True)
	name: Mapped[str] = mapped_column(String(128))
	created_on: Mapped[dt.date] = mapped_column(Date)
	last_edit: Mapped[dt.date] = mapped_column(Date)
	account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))

	account: Mapped['Account'] = relationship(back_populates='journals')
	notes: Mapped['Note'] = relationship(back_populates='journal')

	def __repr__(self):
		return f"journal : {self.id}, {self.name}, {self.created_on}, {self.last_edit}, {self.account_id}"

class Note(Base):
	__tablename__ = "notes"

	id: Mapped[int] = mapped_column(BigInteger, Sequence('journals_id_seq'), primary_key=True)
	date: Mapped[dt.date] = mapped_column(Date)
	name: Mapped[str] = mapped_column(String(128))
	text: Mapped[str] = mapped_column(Text)
	added_on: Mapped[dt.date] = mapped_column(Date)
	journal_id: Mapped[int] = mapped_column(ForeignKey('journals.id'))

	journal: Mapped['Journal'] = relationship(back_populates='notes')

	def __repr__(self):
		return f"note : {self.id}, {self.date}, {self.name}, {self.text}, {self.added_on}, {self.journal_id}"
	
engine = create_engine("postgresql+psycopg2://postgres:123457896_Qq@localhost:5432/postgres")

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
		with Session(engine) as session, session.begin():
			session.add(Account(email=email, password=password, name=name))

	def edit_account(self, id, email, password, name) -> None:
		with Session(engine) as session:
			update_stmt = update(Account).where(Account.id == id).values(
				email=email,
				password=password,
				name=name
			)
			session.execute(update_stmt)
			session.commit()
		
	def delete_account(self, id):
		with Session(engine) as session:
			delete_stmt = delete(Account).where(Account.id == id)
			session.execute(delete_stmt)
			session.commit()

	def get_account(self, id):
		with Session(engine) as session:
			return session.get(Account, id)

	def get_all_accounts(self):
		with Session(engine) as session:
			return session.scalars(select(Account)).all()


	def create_journal(self, name, account_id) -> None:
		with Session(engine) as session, session.begin():
			session.add(Journal(name=name, account_id=account_id, created_on=dt.date.today(), last_edit=dt.date.today()))

	def edit_journal(self, id, name, account_id) -> None:
		with Session(engine) as session:
			update_stmt = update(Journal).where(Journal.id == id).values(
				name=name,
				account_id=account_id,
				last_edit=dt.date.today()
			)
			session.execute(update_stmt)
			session.commit()
		
	def delete_journal(self, id):
		with Session(engine) as session:
			delete_stmt = delete(Journal).where(Journal.id == id)
			session.execute(delete_stmt)
			session.commit()

	def get_journal(self, id):
		with Session(engine) as session:
			return session.get(Journal, id)

	def get_all_journals(self):
		with Session(engine) as session:
			return session.scalars(select(Journal)).all()
		

	def create_note(self, name, date, text, journal_id) -> None:
		with Session(engine) as session, session.begin():
			session.add(Note(name=name, date=date, text=text, journal_id=journal_id, added_on=dt.date.today()))

	def edit_note(self, id, name, date, text, journal_id) -> None:
		with Session(engine) as session:
			update_stmt = update(Note).where(Note.id == id).values(
				name=name,
				date=date,
				text=text,
				journal_id=journal_id
			)
			session.execute(update_stmt)
			session.commit()
		
	def delete_note(self, id):
		with Session(engine) as session:
			delete_stmt = delete(Note).where(Note.id == id)
			session.execute(delete_stmt)
			session.commit()

	def get_note(self, id):
		with Session(engine) as session:
			return session.get(Note, id)

	def get_all_notes(self):
		with Session(engine) as session:
			return session.scalars(select(Note)).all()
		

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