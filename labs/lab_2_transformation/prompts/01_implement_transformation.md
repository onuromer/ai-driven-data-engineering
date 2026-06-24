# Prompt: Implement the dbt Transformation Models

Copy the following prompt into your AI coding assistant:

---

Use skill: implement-tasks

Read the tasks in `docs/tasks/` and implement all **transformation-related tasks**. Build a dbt project that transforms the raw data in DuckDB into clean staging models and analytical marts.

### KEY REQUIREMENTS

- **Location:** All dbt code in `transform/` directory
- **Database:** DuckDB at `data/pokedex.db`
- **Adapter:** Use `dbt-duckdb`
- **Source data:** Raw tables created by dlt in Lab 1

### DBT PROJECT STRUCTURE

```
transform/
├── dbt_project.yml
├── profiles.yml
├── models/
│   ├── staging/
│   │   ├── _staging.yml          # Sources + tests
│   │   ├── stg_pokemon.sql
│   │   ├── stg_types.sql
│   │   ├── stg_abilities.sql
│   │   ├── stg_moves.sql
│   │   └── stg_stats.sql
│   └── marts/
│       ├── _marts.yml            # Model docs + tests
│       ├── fct_pokemon_stats.sql
│       ├── dim_type_effectiveness.sql
│       └── fct_competitive_moves.sql
└── macros/                       # Optional
```

### MODEL SPECIFICATIONS

**Staging Layer** (1:1 mapping of raw tables):
- Rename columns to snake_case
- Cast data types explicitly
- Select only relevant columns
- Add `_loaded_at` timestamp from dlt metadata if available

**Mart Models:**

1. **`fct_pokemon_stats`** — Each Pokemon's base stats with:
   - Individual stats as columns (hp, attack, defense, sp_attack, sp_defense, speed)
   - Calculated BST (Base Stat Total = sum of all stats)
   - Comparison against the average of its primary type (e.g., "Is this Pikachu faster than the average Electric-type?")

2. **`dim_type_effectiveness`** — Type matchup matrix:
   - Columns: `attacking_type`, `defending_type`, `damage_multiplier`
   - Values: 2.0 (super effective), 1.0 (normal), 0.5 (not very effective), 0.0 (immune)

3. **`fct_competitive_moves`** — Move analysis with:
   - Pokemon name, move name, move type, power, accuracy, damage class
   - STAB flag: `true` when the move's type matches one of the Pokemon's types
   - STAB power: if STAB is true, `power * 1.5`

### TESTING

- Define dbt tests in `schema.yml` files:
  - `unique` + `not_null` on primary keys
  - `accepted_values` on type columns
  - `relationships` between marts and staging models
- Create end-to-end tests in `tests/` (pytest) that verify dbt models have data

---

**While the AI works**, observe how it handles:
- Setting up the dbt-duckdb connection (`profiles.yml`)
- Discovering the raw table names created by dlt
- Writing complex SQL (window functions for type-average comparisons, STAB logic)
