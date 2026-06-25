# Product Requirements Document (PRD): Pokemon Conversational Data Agent

## 1. Introduction
The **Pokemon Conversational Data Agent** is a natural language interface built using the Google Agent Development Kit (ADK). It enables users (analysts, developers, and Pokemon enthusiasts) to query Pokemon analytics data stored in Google Cloud BigQuery using plain English.

Currently, querying the data platform requires writing complex SQL joins across multiple tables. This conversational agent democratizes access to the data, allowing users to ask questions about Pokemon stats, type effectiveness, and competitive moves, and receive human-readable, context-aware answers alongside the underlying SQL query executed to retrieve the information.

## 2. Goals
- **Natural Language Data Access**: Enable users to query the Pokemon analytical marts layer using standard English without needing SQL knowledge.
- **Accurate Query Translation**: Accurately translate user queries into valid BigQuery SQL statements that execute against the designated schema.
- **Transparent Execution**: Show both the conversational answer and the underlying SQL query for transparency and validation.
- **Safe Database Operations**: Ensure that the agent only executes read-only query operations, preventing any data modification or schema destruction.
- **Context Preservation**: Handle follow-up questions in the context of the active conversation.

## 3. User Stories
- **As a** Pokemon Analyst,  
  **I want to** ask "Which Electric-type Pokemon has the highest speed stat?" in plain English,  
  **so that** I can quickly retrieve the answer without writing SQL queries.
  
- **As a** Competitive Player,  
  **I want to** ask "What moves are best for Pikachu and do they get STAB bonus?"  
  **so that** I can design optimal move-sets for my competitive battles.

- **As a** Software Developer,  
  **I want to** see the SQL query the agent executed,  
  **so that** I can verify the correctness of the agent's logic and reuse the SQL in other applications.

## 4. Functional Requirements

### 4.1. Core Conversation Engine
- **ADK Integration**: The agent must be constructed using the latest `google-adk` framework.
- **Model Selection**: The agent must use the `gemini-2.5-flash` model.
- **Context and Memory**: The agent must preserve conversation context using `InMemorySessionService` to resolve follow-up queries (e.g., "What about Charizard?").

### 4.2. Database Connection and Tooling
- **BigQuery Toolset**: Use the ADK `BigQueryToolset` for all schema discovery and query executions.
- **Read-Only Access**: Configure the BigQuery tool with a `write_mode=WriteMode.BLOCKED` (or equivalent ADK setting) to enforce SELECT-only commands.
- **Authentication**: Authenticate using GCP Application Default Credentials (ADC). No hardcoded service account keys or credentials.

### 4.3. Marts Schema Support
The system prompt must inject schema context for the following three mart tables:
1. **`fct_pokemon_stats`**:
   - `pokemon_id` (INT64)
   - `pokemon_name` (STRING)
   - `primary_type` (STRING)
   - `secondary_type` (STRING)
   - `hp` (INT64)
   - `attack` (INT64)
   - `defense` (INT64)
   - `sp_attack` (INT64)
   - `sp_defense` (INT64)
   - `speed` (INT64)
   - `base_stat_total` (INT64)
   - `hp_vs_type_avg` (FLOAT64)
   - `attack_vs_type_avg` (FLOAT64)
   - `defense_vs_type_avg` (FLOAT64)
   - `sp_attack_vs_type_avg` (FLOAT64)
   - `sp_defense_vs_type_avg` (FLOAT64)
   - `speed_vs_type_avg` (FLOAT64)
2. **`dim_type_effectiveness`**:
   - `attacking_type` (STRING)
   - `defending_type` (STRING)
   - `damage_multiplier` (FLOAT64) — Possible values: 2.0 (super effective), 1.0 (neutral), 0.5 (not very effective), 0.0 (immune)
3. **`fct_competitive_moves`**:
   - `pokemon_name` (STRING)
   - `move_name` (STRING)
   - `move_type` (STRING)
   - `power` (INT64)
   - `accuracy` (INT64)
   - `damage_class` (STRING)
   - `is_stab` (BOOLEAN)
   - `stab_adjusted_power` (FLOAT64)

### 4.4. CLI Interface (agent/main.py)
- **Interactive Terminal Loop**: Launch a simple command-line interface waiting for user input (`input()`).
- **Response Format**: Display the agent's natural language response and any SQL statements extracted from `execute_sql` tool calls.
- **Graceful Termination**: Exit the loop when the user enters "quit", "exit", or issues a keyboard interrupt (`Ctrl+C`).
- **No Streaming or TUI**: Output must print synchronously/block-by-block. No fancy text-user-interface (TUI) frameworks.

### 4.5. SQL Safety & System Prompt Rules
- **SELECT Enforcement**: Explicitly instruct the agent in the system prompt to *only* generate SELECT statements. Reject any mutation commands (INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER).
- **Fully Qualified Names**: Table references in queries must use the fully qualified format: `{project_id}.{dataset_name}.{table_name}` or `{dataset_name}.{table_name}` derived from environment variables.
- **Example Questions**: The prompt must include the following examples to guide agent behavior:
  - *How does Charizard's attack stat compare to the average fire type?*
  - *What is the damage multiplier when a Water-type Pokemon attacks a Fire-type Pokemon?*
  - *Which competitive moves for Pikachu have STAB (Same Type Attack Bonus) active?*
  - *List the top 5 Pokemon with the highest base stat total.*

## 5. Non-Goals
- **Agent Analytics**: Storing agent run events or performance tracing in BigQuery (BigQueryAgentAnalyticsPlugin) is explicitly out of scope for this version.
- **Web App / UI**: A web dashboard or chat page is out of scope. The interface is strictly a local CLI.
- **Writing/Modifying Data**: The agent will not ingest or transform raw Pokemon data. It is restricted to reading the mart layer.

## 6. Design Considerations
- **CLI Layout**: Keep output clean and easy to scan.
  ```text
  >>> Ask Pokemon Agent: [User input query here]
  
  [SQL Query Executed]:
  SELECT ... FROM ...
  
  [Agent Answer]:
  ...
  ```
- **Error Feedback**: If a query fails or table schemas are mismatched, output a clean user-friendly message rather than a raw Python traceback, while still printing the generated SQL.

## 7. Technical Considerations
- **Code Organization**: All agent source files reside in the `agent/` folder:
  - `agent/main.py` (CLI entry point & conversation loop)
  - `agent/config.py` (Environment variable loading and setup validation)
  - `agent/prompts.py` (System instruction builder incorporating schema and rules)
- **Environment Dependencies**:
  - `GCP_PROJECT_ID`: Target Google Cloud project where BigQuery tables live.
  - `GCP_LOCATION`: Location of Vertex AI and BigQuery datasets (e.g., `us-central1` or `US`).
  - `BQ_DATASET_NAME`: The name of the BigQuery dataset containing the pokemon marts (defaults to `pokedex_marts`).
- **Execution Lifecycle**:
  - The CLI starts, loads configurations, resolves credentials, constructs the `Agent`, binds the `BigQueryToolset`, instantiates the `Runner`, and enters the loop.
  - The runner handles the asynchronous generator loops using `asyncio`.

## 8. Success Metrics
- **Functional Completeness**: The CLI correctly accepts commands, interacts with Gemini, executes SELECTs on BigQuery, and formats responses.
- **Schema Awareness**: The agent demonstrates understanding of stats, type effectiveness, and competitive moves by querying the correct columns and tables.
- **Strict Safety**: 100% of queries executed against BigQuery are read-only.
- **Clean Exit**: The app terminates properly when requesting an exit.

## 9. Open Questions
- None. The scope is well-defined.
