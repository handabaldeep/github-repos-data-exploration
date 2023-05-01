{{ 
    config(
        materialized='incremental',
        unique_key='last_updated'
    ) 
}}

with
repos as (

    select * from {{ ref("stg_repos__last_updated") }}

),

files as (

    select * from {{ source("core", "files") }}

),

contents as (

    select * from {{ source("core", "contents") }}

),

file_contents as (

    select 
        contents.content as content, 
        contents.binary as binary, 
        files.path as path, 
        files.repo_name as repo_name

    from files
    inner join contents
    on files.id = contents.id
    
    where repo_name in (
        select repo_name from {{ ref("stg_repos__last_updated") }}
    )

),

repos_file_contents as (

    select 
        file_contents.repo_name as repo_name, 
        repos.last_updated as last_updated,
        file_contents.path as path,
        file_contents.content as content, 
        file_contents.binary as binary

    from file_contents
    inner join repos
    on file_contents.repo_name = repos.repo_name

)

select * from repos_file_contents

{% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    where last_updated > (select max(last_updated) from {{ this }})
{% endif %}
