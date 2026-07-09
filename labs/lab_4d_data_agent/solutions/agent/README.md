# Pokemon Analytics Conversational Data Agent

An interactive natural language data agent built using the **Google Agent Development Kit (ADK)** and powered by the **Gemini 2.5 Flash** model. It translates natural language user queries into BigQuery SQL statements, executes them against the PokeAPI analytical marts layer, and delivers conversational answers.

## Architecture

The agent is organized into the following modules:
- `agent/config.py`: Validates environment settings.
- `agent/prompts.py`: Defines the system instruction set containing the schema contexts, query translation rules, and safety boundaries.
- `agent/agent.py`: Sets up BigQuery authentication (ADC), toolsets, and instantiates the ADK Agent (optionally registering the analytics plugin).
- `agent/main.py`: Interactive CLI runner wrapping the asynchronous conversation stream.

## Setup & Execution

### Prerequisites

1. Set the Google Cloud credentials to target your project:
   ```bash
   export GCP_PROJECT_ID="your-gcp-project-id"
   export GCP_LOCATION="us-central1"
   export BQ_DATASET_NAME="pokedex_marts"
   ```
2. Verify you have authenticated via Application Default Credentials (ADC):
   ```bash
   gcloud auth application-default login
   ```

### Execution

To launch the interactive CLI loop:
```bash
uv run python agent/main.py
```

To exit the loop, type `exit` or `quit`.

### Running Tests

To run the automated tests (unit and integration tests):
```bash
uv run pytest tests/test_agent.py -v
```

## Example Queries

- *"Which Pokemon has the highest BST?"*
- *"What types are super effective against Steel?"*
- *"Show me the top 5 STAB moves for Gengar"*
- *"How does Charizard's attack stat compare to the average fire type?"*
