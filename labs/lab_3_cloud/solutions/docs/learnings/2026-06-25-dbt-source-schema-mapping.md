---
date: 2026-06-25
topic: dbt Source Schema Mapping for BigQuery
---

# dbt Source Schema Mapping Across Targets

## The Problem / Context
dlt loads data into a dataset named `pokedex_raw` in BigQuery, but the dbt source YAML defined `schema: raw`. dbt's `generate_source_schema_name` macro does NOT exist as a dispatch hook — it's not called by dbt core. This caused "dataset not found" errors.

## The Solution / Learning
Use Jinja directly in the source YAML `schema` field — dbt evaluates Jinja in YAML properties:

```yaml
sources:
  - name: raw
    schema: "{{ 'pokedex_raw' if target.type == 'bigquery' else 'raw' }}"
```

For model output schemas (staging, marts), override `generate_schema_name` in `macros/`:

```sql
{% macro generate_schema_name(custom_schema_name, node) %}
    {%- if target.type == 'bigquery' and custom_schema_name is not none -%}
        pokedex_{{ custom_schema_name | trim }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{% endmacro %}
```

**Key insight:** `generate_source_schema_name` is NOT a real dbt hook. Don't create that macro — it won't be called.
