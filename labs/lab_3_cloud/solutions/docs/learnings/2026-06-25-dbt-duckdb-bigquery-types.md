---
date: 2026-06-25
topic: dbt DuckDB-to-BigQuery Portability
---

# dbt Models: DuckDB ↔ BigQuery Type Compatibility

## The Problem / Context
When porting dbt models from DuckDB (dev) to BigQuery (prod), several SQL type and syntax differences caused all staging models to fail.

## The Solution / Learning

Use dbt's cross-adapter macros instead of raw SQL types:

| DuckDB | BigQuery | dbt Macro |
|--------|----------|-----------|
| `varchar` | `STRING` | `{{ dbt.type_string() }}` |
| `double` | `FLOAT64` | `{{ dbt.type_float() }}` |
| `"order"` (double-quote) | `` `order` `` (backtick) | `{{ adapter.quote('order') }}` |

For `accepted_values` tests on numeric columns, add `quote: false` in the YAML — BigQuery is strict about `FLOAT64 IN ('string')` type mismatches, while DuckDB silently coerces.

```yaml
- accepted_values:
    values: [0.0, 0.5, 1.0, 2.0]
    quote: false
```
