# Runbook: Pokémon Analytics Lakehouse (Ingestion + Transformation)

End-to-end guide for the local-first lakehouse: PokeAPI → dlt (`raw`) → dbt
(`staging` → `marts`) in DuckDB. See the PRD in `docs/prds/` for full scope.

## 1. Prerequisites

- Python 3.11+ (this project's venv is pinned to 3.12 — 3.14 lacks some wheels).
- [`uv`](https://docs.astral.sh/uv/) for env + dependency management.

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
```

## 2. Configuration (environment variables)

| Variable | Default | Meaning |
|----------|---------|---------|
| `POKEMON_LIMIT` | `151` (when unset) | Number of Pokémon **detail pages** to fetch. `0` = full catalog. Types, stats, moves, and abilities are **always** fetched in full regardless. |
| `PIPELINE_DESTINATION` | `duckdb` | dlt destination (only `duckdb` is wired up in this feature). |

Copy `.env.example` → `.env` and adjust as needed.

> **Note:** a full run (`POKEMON_LIMIT=0`) fetches every move's detail
> (~900+ requests) because the marts need move power/accuracy/type/damage_class.
> Expect it to take several minutes. Dev/testing with the default 151 is fast.

## 3. Run the pipeline end-to-end (dev → `data/pokedex.db`)

```bash
# 1. Ingest PokeAPI -> raw schema in DuckDB
uv run python -m ingestion.pipeline

# 2. Transform: build staging views + mart tables, run all dbt tests
cd transform
dbt build --profiles-dir .
```

`dbt build` with the default `dev` target writes to `data/pokedex.db`. Use
`--target test` to point at `data/test_pokedex.db` instead.

## 4. What gets built

**`raw`** (dlt) — 1 table per endpoint plus dlt child tables for nested arrays:
`raw.pokemon`, `raw.types`, `raw.stats`, `raw.abilities`, `raw.moves`,
`raw.pokemon__{stats,types,moves}`, `raw.types__damage_relations__*`.

**`staging`** (dbt views) — typed 1:1 cleans: `stg_pokemon`, `stg_types`,
`stg_stats`, `stg_abilities`, `stg_moves`, plus unpacked child views
`stg_pokemon_{stats,types,moves}` and `stg_type_damage_relations`.

**`marts`** (dbt tables):

| Model | Grain | Highlights |
|-------|-------|------------|
| `fct_pokemon_stats` | 1 row / Pokémon | 6 stat columns, `bst`, per-stat `_vs_type_avg` delta vs. the average for the Pokémon's **primary** type |
| `dim_type_effectiveness` | 1 row / (attacking, defending) | Dense **18×18** matrix (324 rows); `damage_multiplier` ∈ {2.0, 1.0, 0.5, 0.0}; unlisted pairs default to 1.0 |
| `fct_competitive_moves` | 1 row / (Pokémon, move) | **All** learnable moves (no filter); `is_stab` (move type matches primary OR secondary); `stab_adjusted_power` = `power × 1.5` when STAB, `NULL` for status/no-power moves |

The 18×18 grid spine comes from the `pokemon_types` seed (18 standard types),
so completeness is independent of what was ingested.

## 5. Testing

```bash
uv run pytest tests/ -v
```

Tests are **fully offline and deterministic** — PokeAPI is mocked with
`responses` and everything runs against `data/test_pokedex.db` (never the dev DB).

- `test_config.py` — `POKEMON_LIMIT` / destination resolution
- `test_pokeapi_client.py` — pagination (`next`), 429 backoff / `Retry-After`
- `test_pokeapi_source.py` — resource generators, limit behaviour
- `test_pipeline.py` — raw tables, nested child-table unpack, merge idempotency
- `test_transform_e2e.py` — full ingestion → `dbt build` → mart-correctness
  (324-row matrix, `bst` = stat sum, STAB flag + adjusted power, status NULL)

## 6. Operational notes

- **profiles.yml lives in `transform/`** — always pass `--profiles-dir .` (or set
  `DBT_PROFILES_DIR`). Medallion schemas (`staging`/`marts`) come from a custom
  `generate_schema_name` macro so they aren't prefixed.
- **Idempotency:** dlt resources use `write_disposition="merge"` on `primary_key`,
  so re-running ingestion upserts rather than duplicating.
- **Windows/antivirus:** dlt's normalize/load step can hit transient
  `WinError 5` (access denied) when AV scans temp files. `ingestion/pipeline.py`
  recovers automatically by dropping the pending package and re-running (safe
  under merge). If `uv run pytest` can't spawn `pytest.exe`, use
  `uv run python -m pytest` (a trampoline-install glitch, same AV cause).
