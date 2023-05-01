/* We create an incremental model such that when new data arrives
we will only add rows created after the last updated date.
With the unique_key parameter we ensure that the existing repos
are updated with their latest updated date. */
{{ 
    config(
        materialized='incremental',
        unique_key='last_updated'
    ) 
}}

with repos as (

    select 
        DATE(TIMESTAMP_SECONDS(max(committer.time_sec))) as last_updated,
        repo_name

    from {{ source("staging", "commits") }},
    unnest(repo_name) as repo_name

    where repo_name in (
        select repo_name from {{ ref('stg_repos__python') }}
    )

    group by repo_name

)

select 
    repo_name,
    last_updated

from repos

where last_updated <= CURRENT_DATE()
{% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    and last_updated > (select max(last_updated) from {{ this }})
{% endif %}

order by last_updated desc
