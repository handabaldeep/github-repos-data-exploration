select * from {{ ref("repos__file_contents_last_updated") }}

where last_updated between "2022-01-01" and "2022-03-31"

-- To skip this: dbt build -m <model.sql> --vars 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 1000

{% endif %}
