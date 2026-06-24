---
date: 2026-06-24
topic: DLT Credentials and Mock Matching
---

# DLT Credentials and Mock Matching

## The Problem / Context
During implementation of the PokeAPI dlt ingestion pipeline, we encountered two main issues:
1. `dlt.pipeline(...)` threw a `TypeError` when we passed `credentials=f"duckdb:///{db_path}"` directly.
2. The mock integration tests using the `responses` library failed with connection errors because the request URLs in `pipeline.py` did not match the query parameters in the registered mocks (i.e. `https://pokeapi.co/api/v2/type/` vs `https://pokeapi.co/api/v2/type/?limit=100`).

## The Solution / Learning
1. **DLT Credentials**: Connection credentials and database paths should be passed to `pipeline.run(source, credentials=...)` instead of `dlt.pipeline(...)` in recent versions of `dlt`.
2. **Responses Parameter Matching**: When mocking requests with `responses`, query parameters must match exactly. Adding `?limit=100` to the pipeline URLs resolved the mismatch, minimized the number of live API requests, and successfully aligned the mock tests.
3. **Selective Ingestion Limits**: By implementing `POKEMON_LIMIT` parsing and passing it to the generator-based `fetch_pokemon` resource, we can enforce dev-limits while keeping lookup catalogs (types, moves, abilities) fully populated.
