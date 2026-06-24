---
date: 2026-06-24
topic: dbt-duckdb schema naming for medallion layers
---

# dbt-duckdb creates `main_staging` instead of `staging`

## The Problem / Context

When configuring dbt models with `+schema: staging` and `+schema: marts` in `dbt_project.yml`, dbt-duckdb placed models in `main_staging` and `main_marts` rather than the `staging` and `marts` schemas expected by the medallion architecture (and referenced in the PRD).

## The Solution / Learning

Override the default `generate_schema_name` macro so custom schema names are used as-is:

```sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
```

Place this in `transform/macros/generate_schema_name.sql`. After adding it, models land in `staging.stg_pokemon` and `marts.fct_pokemon_stats` as intended.

Also set `profiles.yml` paths relative to the transform directory (e.g. `../data/pokedex.db`) and use `--profiles-dir .` when running dbt from `transform/`.
