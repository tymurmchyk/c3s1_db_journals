with vars as (
	select
		10000 as n,
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