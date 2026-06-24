# Lab 1 — Reference Solution

## Files

- `ingestion/pipeline.py` — dlt pipeline with generator-based resources, pagination, retry on 429, and `POKEMON_LIMIT` support
- `tests/test_pipeline.py` — Mocked integration tests for ingestion, limit enforcement, and retry backoff

## Generating the Data

The DuckDB database is not included in the solution (binary files don't belong in git). To generate it:

```bash
# Default: 151 Pokemon
uv run python ingestion/pipeline.py

# Custom limit
POKEMON_LIMIT=10 uv run python ingestion/pipeline.py
```

This creates `data/pokedex.db` with the `raw` schema containing all ingested tables.

## Verifying the Data

```bash
uv run python -c "
import duckdb
conn = duckdb.connect('data/pokedex.db')
tables = conn.execute(\"SELECT table_name, estimated_size FROM duckdb_tables() WHERE schema_name = 'raw'\").fetchall()
for name, size in tables:
    count = conn.execute(f'SELECT COUNT(*) FROM raw.{name}').fetchone()[0]
    print(f'  raw.{name}: {count} rows')
conn.close()
"
```
