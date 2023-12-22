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
where (j.last_edit >= '2023-5-1') and (j.last_edit <= '2023-6-20')
group by a.id, j.id, n.id
order by j.last_edit, a.id