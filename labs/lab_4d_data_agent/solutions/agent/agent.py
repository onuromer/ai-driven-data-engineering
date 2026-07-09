import os
import logging
import google.auth

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.integrations.bigquery import BigQueryToolset, BigQueryCredentialsConfig
from google.adk.integrations.bigquery.config import BigQueryToolConfig, WriteMode
from google.adk.plugins.bigquery_agent_analytics_plugin import BigQueryAgentAnalyticsPlugin, BigQueryLoggerConfig

from agent.config import load_config
from agent.prompts import get_system_prompt

logger = logging.getLogger("pokemon_agent.agent")

def initialize_agent_and_runner(session_service):
    """
    Initializes the ADK Agent, BigQuery Toolset, and Runner.
    Enforces read-only BigQuery access.
    Optionally configures BigQuery Agent Analytics logging if BQ_ANALYTICS_DATASET_NAME is set.
    """
    # 1. Load configuration
    config = load_config()
    project_id = config["GCP_PROJECT_ID"]
    location = config["GCP_LOCATION"]
    dataset_name = config["BQ_DATASET_NAME"]
    
    # Set environment variables for Google GenAI / Vertex AI integration
    os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
    os.environ['GOOGLE_CLOUD_LOCATION'] = location
    os.environ['GOOGLE_GENAI_USE_ENTERPRISE'] = 'True'
    
    logger.info("Initializing Agent Core...")
    
    # 2. Get Application Default Credentials (ADC) for BigQuery
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials_config = BigQueryCredentialsConfig(credentials=credentials)
    
    # 3. Configure BQ Toolset (Enforce Read-Only safety)
    tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)
    bigquery_toolset = BigQueryToolset(
        credentials_config=credentials_config,
        bigquery_tool_config=tool_config
    )
    
    # 4. Generate system prompt
    system_prompt = get_system_prompt(project_id, dataset_name)
    
    # 5. Define ADK Agent
    pokemon_agent = Agent(
        model="gemini-2.5-flash",
        name="pokemon_analytics_agent",
        description="Conversational agent for querying Pokemon stats, type effectiveness, and moves in BigQuery.",
        instruction=system_prompt,
        tools=[bigquery_toolset]
    )
    
    # 6. Check for Analytics Plugin (Optional)
    analytics_dataset = os.environ.get("BQ_ANALYTICS_DATASET_NAME")
    app = None
    
    if analytics_dataset:
        logger.info(f"Configuring Agent Analytics with BigQuery dataset: {analytics_dataset}")
        
        # Configure logging settings
        gcs_bucket = os.environ.get("GCS_BUCKET_NAME")
        bq_logger_config = BigQueryLoggerConfig(
            enabled=True,
            gcs_bucket_name=gcs_bucket,  # Optional GCS offloading
            log_multi_modal_content=True,
            max_content_length=500 * 1024,
            batch_size=1,
            shutdown_timeout=10.0
        )
        
        # Instantiate plugin
        bq_logging_plugin = BigQueryAgentAnalyticsPlugin(
            project_id=project_id,
            dataset_id=analytics_dataset,
            table_id="agent_events",
            config=bq_logger_config,
            location=location
        )
        
        # Create App to attach plugin
        app = App(
            name="pokemon_analytics_app",
            root_agent=pokemon_agent,
            plugins=[bq_logging_plugin]
        )
        
        # Return runner with App
        logger.info("Runner initialized with App and Analytics Plugin.")
        return Runner(app=app, session_service=session_service)
        
    else:
        # Return runner directly with Agent
        logger.info("Runner initialized with Agent directly (analytics disabled).")
        return Runner(
            agent=pokemon_agent,
            app_name="pokemon_analytics_app",
            session_service=session_service
        )

# =====================================================================
# Global definitions for ADK Web CLI / Dev UI discovery
# =====================================================================
root_agent = None

if os.environ.get("GCP_PROJECT_ID"):
    try:
        _config = load_config()
        _project_id = _config["GCP_PROJECT_ID"]
        _location = _config["GCP_LOCATION"]
        _dataset_name = _config["BQ_DATASET_NAME"]
        
        os.environ['GOOGLE_CLOUD_PROJECT'] = _project_id
        os.environ['GOOGLE_CLOUD_LOCATION'] = _location
        os.environ['GOOGLE_GENAI_USE_ENTERPRISE'] = 'True'
        
        _credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        _credentials_config = BigQueryCredentialsConfig(credentials=_credentials)
        
        _tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)
        _bigquery_toolset = BigQueryToolset(
            credentials_config=_credentials_config,
            bigquery_tool_config=_tool_config
        )
        
        _system_prompt = get_system_prompt(_project_id, _dataset_name)
        
        root_agent = Agent(
            model="gemini-2.5-flash",
            name="pokemon_analytics_agent",
            description="Conversational agent for querying Pokemon stats, type effectiveness, and moves in BigQuery.",
            instruction=_system_prompt,
            tools=[_bigquery_toolset]
        )
        
        _analytics_dataset = os.environ.get("BQ_ANALYTICS_DATASET_NAME")
        if _analytics_dataset:
            _gcs_bucket = os.environ.get("GCS_BUCKET_NAME")
            _bq_logger_config = BigQueryLoggerConfig(
                enabled=True,
                gcs_bucket_name=_gcs_bucket,
                log_multi_modal_content=True,
                max_content_length=500 * 1024,
                batch_size=1,
                shutdown_timeout=10.0
            )
            _bq_logging_plugin = BigQueryAgentAnalyticsPlugin(
                project_id=_project_id,
                dataset_id=_analytics_dataset,
                table_id="agent_events",
                config=_bq_logger_config,
                location=_location
            )
            app = App(
                name="pokemon_analytics_app",
                root_agent=root_agent,
                plugins=[_bq_logging_plugin]
            )
    except Exception as _e:
        logger.warning(f"Could not pre-initialize root_agent at module level: {_e}")

