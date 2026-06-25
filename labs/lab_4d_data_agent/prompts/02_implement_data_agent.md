# Prompt: Implement the Data Agent

Copy the prompt below into your AI coding assistant.

~~~
Use skill: implement-tasks

Read the data agent tasks in docs/tasks/ and implement the ADK-based data agent.

Important: Before implementing, read the Google ADK documentation in docs/knowledge/google-adk.txt for API patterns, agent configuration, and tool setup. This file contains the latest ADK documentation.

KEY REQUIREMENTS

- Framework: Google Agent Development Kit (google-adk)
- Model: gemini-2.5-flash (or latest available)
- Location: All code in agent/ directory
- Data source: BigQuery marts layer (fct_pokemon_stats, dim_type_effectiveness, fct_competitive_moves)
- The agent will be run using the ADK Web UI (adk web), NOT a custom CLI runner

AGENT STRUCTURE

The agent must follow the ADK standard directory layout so "adk web" can auto-discover it, AND include a CLI runner as an alternative:

agent/
├── __init__.py          # Must export "root_agent" (the ADK Agent instance) for adk web
├── agent.py             # Agent definition with BigQuery toolset
├── main.py              # CLI runner (alternative to adk web)
└── prompts.py           # System prompt with data model context

Important: The ADK Web UI ("adk web agent") expects the agent package to expose a "root_agent" variable in __init__.py. This is how adk web discovers and loads the agent. The CLI runner (main.py) is an alternative for terminal-based interaction.

IMPLEMENTATION

1. Agent Definition (agent.py):
   - Create an ADK Agent with Gemini model
   - Use the ADK BigQuery Toolset for SQL execution with WriteMode.BLOCKED (read-only)
   - Configure with GCP project ID and dataset from environment variables
   - Use Application Default Credentials (ADC)
   - Return the agent instance

2. Package Init (__init__.py):
   - Import the agent from agent.py
   - Expose it as "root_agent" so "adk web" can discover it

3. System Prompt (prompts.py):
   - Describe the available tables and their columns:
     * fct_pokemon_stats: pokemon_id, pokemon_name, primary_type, secondary_type, hp, attack, defense, sp_attack, sp_defense, speed, base_stat_total, *_vs_type_avg columns
     * dim_type_effectiveness: attacking_type, defending_type, damage_multiplier
     * fct_competitive_moves: pokemon_name, move_name, move_type, power, accuracy, damage_class, is_stab, stab_adjusted_power
   - Include fully qualified BigQuery table names using project ID and dataset from env vars
   - Add example questions the agent can answer
   - Include SELECT-only safety constraint in the prompt

4. Environment Variables:
   - GCP_PROJECT_ID (required): The GCP project ID
   - GCP_LOCATION (optional, default: us-central1): Region for Vertex AI
   - BQ_DATASET_NAME (optional, default: pokedex_marts): BigQuery dataset name

TESTING

- Verify the agent starts without errors: "adk web agent"
- Test with sample questions in the Web UI:
  * "Which Pokemon has the highest BST?"
  * "What types are super effective against Steel?"
  * "Show me the top 5 STAB moves for Gengar"
~~~

## While the AI Works

Observe how it:
- Configures the BigQuery toolset with ADK
- Writes the system prompt (does it include enough schema context?)
- Structures the agent package for `adk web` discovery
- Uses docs/knowledge/google-adk.txt for the latest ADK API patterns
