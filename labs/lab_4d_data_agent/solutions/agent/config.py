import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the project root .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger("pokemon_agent.config")

class ConfigError(ValueError):
    """Exception raised for configuration errors (e.g., missing environment variables)."""
    pass

def load_config():
    """
    Loads and validates the environment variables for the Pokemon Conversational Data Agent.
    
    Required:
      - GCP_PROJECT_ID: The Google Cloud project ID.
      
    Optional (with defaults):
      - GCP_LOCATION: The region/location for BigQuery and Vertex AI (default: "us-central1").
      - BQ_DATASET_NAME: The dataset name containing the Pokemon marts (default: "pokedex_marts").
    
    Returns:
      dict: A dictionary of loaded and validated configurations.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ConfigError("GCP_PROJECT_ID environment variable is required but not set.")
        
    location = os.environ.get("GCP_LOCATION", "us-central1")
    dataset_name = os.environ.get("BQ_DATASET_NAME", "pokedex_marts")
    
    logger.info("Configuration successfully loaded.")
    logger.debug(f"Project ID: {project_id}, Location: {location}, Dataset Name: {dataset_name}")
    
    return {
        "GCP_PROJECT_ID": project_id,
        "GCP_LOCATION": location,
        "BQ_DATASET_NAME": dataset_name
    }
