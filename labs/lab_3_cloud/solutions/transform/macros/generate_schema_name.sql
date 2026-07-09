{% macro generate_schema_name(custom_schema_name, node) -%}
    {#-
        Controls which schema/dataset dbt models land in.
        - DuckDB (dev/test): uses the custom schema name as-is (e.g. 'staging', 'marts')
        - BigQuery (prod): prefixes with 'pokedex_' to match Terraform-provisioned datasets
          (e.g. 'staging' → 'pokedex_staging', 'marts' → 'pokedex_marts')
    -#}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- elif target.type == 'bigquery' -%}
        pokedex_{{ custom_schema_name | trim }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
