---
date: 2026-06-24
topic: dlt schema evolution and dbt test fixtures
---

# dlt child tables and minimal mocks break dbt staging models

## The Problem / Context

End-to-end pytest tests that run mock dlt ingestion followed by `dbt build` failed with errors like:

- `Binder Error: Table "pokemon" does not have a column named "base_experience"` — minimal PokeAPI JSON mocks produce a narrower dlt schema than full API responses.
- `Catalog Error: Table types__damage_relations__half_damage_to does not exist` — dlt only creates nested child tables when at least one record has a non-empty array for that relation.
- `assert_dim_type_effectiveness_row_count` failed on test DB — the 324-row test assumes all 18 standard types are ingested.

## The Solution / Learning

**Staging models:** Only select columns that exist in both full and minimal ingestion payloads, or enrich test mocks to include every flattened field the staging SQL references (`base_experience`, `generation__name`, `pp`, etc.).

**dlt nested tables:** If a mart joins `raw.types__damage_relations__*`, test mocks must include at least one non-empty damage relation array per table type (e.g. one `half_damage_to` entry) so dlt materializes the child table.

**pytest + dbt:** Use `dbt run` (not `dbt build`) in test fixtures when the test database has a subset of types. Assert matrix size as `n × n` for the types present, and reserve full-data singular tests (like the 324-row check) for `dbt build` against `data/pokedex.db`.

**Optional columns:** Do not reference rarely populated flattened fields (e.g. `stats.move_damage_class__name`) in staging unless they are guaranteed by ingestion — the column may exist in production data but not in minimal test schemas.
