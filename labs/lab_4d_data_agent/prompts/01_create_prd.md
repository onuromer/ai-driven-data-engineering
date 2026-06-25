# Prompt: Create PRD for the Data Agent

Copy the prompt below into your AI coding assistant.

~~~
Act as a Senior AI Engineer. Create a Product Requirements Document (PRD) for a conversational data agent.

Use skill: create-prd

Important: The scope below is already well-defined. Only ask clarifying questions about areas that are genuinely ambiguous or missing. If everything is clear, proceed directly to generating the PRD.

FEATURE SCOPE

Build a conversational data agent using the Google Agent Development Kit (ADK) that allows users to query the Pokemon analytics data in BigQuery using natural language. The agent generates and executes SQL queries against the mart models.

REQUIREMENTS

Agent Core:
- Use Google ADK (google-adk) with the Gemini model (gemini-2.5-flash)
- Connect to BigQuery using the ADK BigQuery Toolset
- The agent should query the marts layer: fct_pokemon_stats, dim_type_effectiveness, fct_competitive_moves
- Use Application Default Credentials for BigQuery authentication
- Location: All agent code in agent/ directory

System Prompt:
- Include the full schema context for all three mart tables:
  * fct_pokemon_stats: pokemon_id, pokemon_name, primary_type, secondary_type, hp, attack, defense, sp_attack, sp_defense, speed, base_stat_total, hp_vs_type_avg, attack_vs_type_avg, defense_vs_type_avg, sp_attack_vs_type_avg, sp_defense_vs_type_avg, speed_vs_type_avg
  * dim_type_effectiveness: attacking_type, defending_type, damage_multiplier (values: 2.0, 1.0, 0.5, 0.0)
  * fct_competitive_moves: pokemon_name, move_name, move_type, power, accuracy, damage_class, is_stab, stab_adjusted_power
- Instruct the agent to always use the fully qualified BigQuery table names with the dataset prefix (e.g., pokedex_marts.fct_pokemon_stats)
- The dataset prefix should come from an environment variable (GCP_PROJECT_ID and dataset name)
- Include 3-5 example questions the agent can answer

CLI Runner (agent/main.py):
- Interactive CLI with a simple input loop (input() → agent response → print)
- Print both the agent's natural language answer and any SQL queries it executed
- Exit on "quit", "exit", or Ctrl+C
- Keep it simple — no fancy TUI, no streaming, just input/print
- Use async conversation with the ADK runner

Agent Capabilities:
- Answer questions about Pokemon stats, type effectiveness, and competitive moves
- Generate and execute SQL queries against BigQuery
- Return results in a conversational, human-readable format
- Handle follow-up questions in context

SQL Safety:
- The agent should only execute SELECT queries — no INSERT, UPDATE, DELETE, DROP
- Include this constraint in the system prompt
- No additional guardrails needed beyond the system prompt instruction

Agent Analytics:
- Agent Analytics is OUT OF SCOPE for this lab — do not implement it
- Keep the agent simple and focused on querying data

TECHNICAL CONSTRAINTS

- Use the latest Google ADK version (check docs/knowledge/google-adk.txt for API patterns)
- The agent must work with the BigQuery datasets created by Terraform in Lab 3
- Use environment variables for GCP project (GCP_PROJECT_ID) and location (GCP_LOCATION)
- No hardcoded credentials or project IDs
~~~
