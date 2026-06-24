# Prompt: Implement the Ingestion Pipeline

Copy the following prompt into your AI coding assistant:

---

Use skill: implement-tasks

Read the tasks in `docs/tasks/` and implement all **ingestion-related tasks**. Focus on building the dlt pipeline that extracts data from the PokeAPI and loads it into a local DuckDB database.

### KEY REQUIREMENTS

- **Source:** PokeAPI REST API (`https://pokeapi.co/api/v2/`)
- **Endpoints:** `pokemon`, `types`, `abilities`, `moves`, `stats`
- **Destination:** Local DuckDB at `data/pokedex.db`
- **Location:** All ingestion code in `ingestion/` directory
- **Framework:** Use `dlt` with the following patterns:
  - Generator-based resources for each endpoint
  - `primary_key` on each resource for idempotency
  - `write_disposition="merge"` for safe re-runs
  - Let dlt handle nested JSON via auto-schema evolution

### IMPLEMENTATION NOTES

- Start with a `pokemon` resource to verify the pipeline works, then add remaining endpoints
- Use `requests` to call the PokeAPI — handle pagination (the API returns paginated lists)
- Add basic error handling for HTTP errors and rate limiting (429)
- Create a main pipeline script at `ingestion/pipeline.py` that can be run directly

### TESTING

- Create end-to-end tests in `tests/` using pytest
- Tests should run the pipeline against the real PokeAPI and verify:
  - Tables are created in DuckDB
  - Row counts are greater than zero
  - Key columns exist (e.g., `id`, `name`)

---

**While the AI works**, observe how it:
- Structures the dlt source and resources
- Handles the PokeAPI's paginated responses
- Deals with nested JSON data (Pokemon stats, type arrays)

If the AI asks questions, answer based on the PRD in `docs/prds/`.
