# Prompt: Create the Project PRD

Copy the following prompt into your AI coding assistant:

---

Act as a Senior Data Architect. Create the Product Requirements Document (PRD) for a new data analytics project.

Use skill: create-prd

### PROJECT OVERVIEW

Build a local-first data lakehouse for competitive Pokemon analytics using Python 3.11+, modern open-source frameworks, and a medallion architecture.

- **Source:** PokeAPI REST API (https://pokeapi.co/api/v2/)
- **Target (Dev):** Local DuckDB (`data/pokedex.db`)
- **Target (Prod):** Google BigQuery (to be set up in a later feature)
- **Architecture:** Raw (dlt) → Staging (dbt) → Marts (dbt)

### FEATURE SCOPE

The PRD should cover two features that will be implemented together:

**Feature 1 — Data Ingestion (dlt)**
- Extract data from PokeAPI REST endpoints: `pokemon`, `types`, `abilities`, `moves`, `stats`
- Load into local DuckDB using dlt
- Use dlt's `primary_key` and `write_disposition="merge"` for idempotency
- Handle nested JSON (e.g., Pokemon stats, type arrays) through dlt's schema evolution
- Implement a generator-based resource approach

**Feature 2 — Data Transformation (dbt)**
- Staging layer: Clean, typed, 1:1 mappings of raw dlt tables
- Marts layer with analytical models:
  - `fct_pokemon_stats` — Base stats with BST (Base Stat Total) and per-type average comparisons
  - `dim_type_effectiveness` — Complete type matchup matrix (2x, 0.5x, 0x)
  - `fct_competitive_moves` — Move pool analysis with STAB (Same Type Attack Bonus) calculation
- dbt tests for uniqueness, not-null, accepted values, and relationship integrity

### TECHNICAL REQUIREMENTS

1. **Project Structure:**
   - `ingestion/` — dlt sources and pipeline scripts
   - `transform/` — dbt project (models, tests, macros, schema.yml)
   - `data/` — DuckDB database file (gitignored)
   - `tests/` — End-to-end and integration tests (pytest)
   - `docs/prds/` — PRD files
   - `docs/tasks/` — Task breakdowns

2. **Python:** 3.11+, managed with `uv`
3. **Dependencies:** `dlt[duckdb]`, `dbt-core`, `dbt-duckdb`, `pytest`, `requests`
4. **Testing:** End-to-end tests that run the pipeline and validate data in DuckDB
5. **Schemas:** Keep `raw` data in a separate schema from `staging` and `marts`

### NON-GOALS (for now)
- Cloud deployment (BigQuery, Terraform) — covered in a later feature
- Pipeline orchestration (Airflow) — covered in a later feature
- Visualization (Streamlit) — covered in a later feature

---

**After the AI asks clarifying questions**, answer them based on the scope above. Focus on keeping the scope tight — we want a working local pipeline with meaningful transformations, not an exhaustive data platform.
