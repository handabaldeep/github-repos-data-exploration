select
    repo_name

from {{ source("staging", "languages") }}

where language[SAFE_OFFSET(0)].name='Python'
