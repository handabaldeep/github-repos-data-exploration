select * from {{ ref("repos__file_contents_last_updated") }}

where last_updated between "2022-01-01" and "2022-03-31"

LIMIT 50000
