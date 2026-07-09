# Task List: Pokemon Conversational Data Agent

This task list details the implementation of the Pokemon Conversational Data Agent based on the [prd-pokemon-agent.md](file:///Users/saschadi/GitHub/ai-driven-data-engineering/tmp/starter-4d/docs/prds/prd-pokemon-agent.md).

## Relevant Files

- `requirements.txt` - Modify to add `google-adk` package dependency.
- `agent/config.py` - Configuration parsing and environment check module (New).
- `agent/prompts.py` - Prompt template definitions containing table schemas, example questions, and constraints (New).
- `agent/agent_core.py` - ADK Agent and BigQuery Toolset configuration module (New).
- `agent/main.py` - Asynchronous CLI conversation loop runner (New).
- `agent/README.md` - Documentation of setup instructions, parameters, and example queries (New).
- `tests/test_agent.py` - Automated test suite for configuration, prompting, safety, and runner behavior (New).

### Notes

- Each parent task represents a complete vertical slice (code + tests + observability + docs).
- Tests must be executed using `uv run pytest tests/test_agent.py`.
- No credentials or project IDs should be hardcoded in any script.

## Tasks

- [x] 1.0 Environment Setup and ADK Dependency Integration (Complete Vertical Slice)
  - [x] 1.1 Append `google-adk` to `requirements.txt`.
  - [x] 1.2 Implement `agent/config.py` to parse and validate `GCP_PROJECT_ID`, `GCP_LOCATION`, and `BQ_DATASET_NAME` environment variables.
  - [x] 1.3 Write a test case in `tests/test_agent.py` verifying that missing environment variables raise appropriate configuration errors.
  - [x] 1.4 Add standard logging to print warning messages if optional configurations default to fallback parameters.
  - [x] 1.5 Add initial setup and environment variable configuration instructions to `agent/README.md`.
- [x] 2.0 System Prompt and Schema Context Construction (Complete Vertical Slice)
  - [x] 2.1 Implement `agent/prompts.py` to construct system prompts detailing the three marts table schemas (`fct_pokemon_stats`, `dim_type_effectiveness`, `fct_competitive_moves`), enforcing fully qualified table names and SELECT-only safety constraints.
  - [x] 2.2 Write a test case in `tests/test_agent.py` verifying that the generated system prompt correctly resolves the dataset prefix and includes key column/table names.
  - [x] 2.3 Integrate standard logging to output the system prompt at level `DEBUG` during initialization.
  - [x] 2.4 Document the prompt engineering rules and schema definitions in `agent/README.md`.
- [x] 3.0 Agent Core & BigQuery Toolset Integration (Complete Vertical Slice)
  - [x] 3.1 Implement `agent/agent.py` to instantiate the ADK `Agent` with `gemini-2.5-flash` and `BigQueryToolset`, enforcing Application Default Credentials (ADC).
  - [x] 3.2 Write a test case in `tests/test_agent.py` verifying that `BigQueryToolset` is properly registered as an active tool on the agent.
  - [x] 3.3 Add logging inside `agent/agent.py` to trace credential resolution and agent assembly steps.
  - [x] 3.4 Document the Python imports, classes, and setup structure in `agent/README.md`.
- [x] 4.0 CLI Runner and Event Interception Loop (Complete Vertical Slice)
  - [x] 4.1 Implement `agent/main.py` conversation loop utilizing ADK `Runner` and `InMemorySessionService`. Intercept events to capture and print SQL statement tool arguments from `execute_sql` tool calls.
  - [x] 4.2 Write a test case in `tests/test_agent.py` verifying that the event parser correctly extracts and displays SQL commands from mock `execute_sql` tool call events.
  - [x] 4.3 Add logger instrumentation to track loop start, loop end, execution latency, and error events.
  - [x] 4.4 Add instructions in `agent/README.md` explaining how to execute the CLI and explaining commands to exit (`quit`/`exit`).
- [x] 5.0 End-to-End Integration and Safety Testing (Complete Vertical Slice)
  - [x] 5.1 Write integration tests in `tests/test_agent.py` simulating queries to check the happy path (valid answers returned) and safety violations (queries requesting UPDATE or DELETE).
  - [x] 5.2 Add specific assertions in test cases verifying that non-SELECT operations are blocked at the prompt level.
  - [x] 5.3 Implement diagnostic execution logs documenting test run success, elapsed time, and exceptions.
  - [x] 5.4 Finalize documentation in `agent/README.md` with execution examples, safety verification guidelines, and troubleshooting scenarios.

