# Prompt: Create PRD for the Data Agent

Copy the prompt below into your AI coding assistant.

~~~
Act as a Senior AI Engineer. Create a Product Requirements Document (PRD) for a conversational data agent.

Use skill: create-prd

FEATURE SCOPE

Build a conversational data agent using the Google Agent Development Kit (ADK) that allows users to query the Pokemon analytics data in BigQuery using natural language. The agent generates and executes SQL queries against the mart models.

REQUIREMENTS

Agent Core:
- Use Google ADK (google-adk) with the Gemini model (e.g., gemini-2.5-flash)
- Connect to BigQuery using the ADK BigQuery Toolset
- The agent should query the marts layer: fct_pokemon_stats, dim_type_effectiveness, fct_competitive_moves
- Use Application Default Credentials for BigQuery authentication
- Location: All agent code in agent/ directory

System Prompt:
- Include the data model context: table names, key columns, relationships
- Describe what each mart table contains so the agent generates accurate SQL
- Include example questions the agent can answer
- Instruct the agent to always use the correct BigQuery dataset prefix (e.g., pokedex_marts)

Agent Capabilities:
- Answer questions about Pokemon stats, type effectiveness, and competitive moves
- Generate and execute SQL queries against BigQuery
- Return results in a conversational format
- Handle follow-up questions in context

Runner:
- Create a CLI runner (agent/main.py) that starts an interactive session
- Support async conversation loop with the agent

Optional — Agent Analytics:
- Add the BigQuery Agent Analytics plugin to log agent events (LLM calls, tool executions, errors) back to BigQuery for observability
- This helps monitor agent performance and debug issues

TECHNICAL CONSTRAINTS

- Use Google ADK 1.x or 2.x (check latest via Context7)
- The agent must work with the BigQuery datasets created by Terraform in Lab 3
- Use environment variables for GCP project and dataset configuration
- No hardcoded credentials
~~~
