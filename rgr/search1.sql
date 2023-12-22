select
	a.id as "account",
	a.email,
	j.id as "journal",
	j.name as "journal name",
	count(n.journal_id) as "notes in journal"
from accounts a
join journals j on a.id = j.account_id
join notes n on j.id = n.journal_id
where (j.created_on >= '2023-5-1') and (j.created_on <= '2023-5-10')
group by a.id, j.id, n.journal_id
order by a.id