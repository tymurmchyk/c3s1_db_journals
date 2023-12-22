select
	count(n.journal_id) as "notes count",
	j.id as "journal",
	j.created_on as "created on",
	j.name
from accounts a
join journals j on a.id=j.account_id
join notes n on j.id=n.journal_id
where (n.added_on >= '2023-5-1') and (n.added_on <= '2023-6-20')
group by j.id, j.created_on, n.journal_id
order by "notes count" desc, j.created_on