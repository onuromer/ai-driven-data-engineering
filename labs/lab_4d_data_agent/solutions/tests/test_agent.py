import os
import pytest
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from agent.config import load_config, ConfigError
from agent.prompts import get_system_prompt
from agent.agent import initialize_agent_and_runner

def test_config_load_success(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "test-project-123")
    monkeypatch.setenv("GCP_LOCATION", "us-east1")
    monkeypatch.setenv("BQ_DATASET_NAME", "custom_marts")
    
    config = load_config()
    
    assert config["GCP_PROJECT_ID"] == "test-project-123", f"Expected project ID test-project-123 but got {config['GCP_PROJECT_ID']}"
    assert config["GCP_LOCATION"] == "us-east1", f"Expected location us-east1 but got {config['GCP_LOCATION']}"
    assert config["BQ_DATASET_NAME"] == "custom_marts", f"Expected dataset custom_marts but got {config['BQ_DATASET_NAME']}"

def test_config_load_defaults(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "test-project-123")
    monkeypatch.delenv("GCP_LOCATION", raising=False)
    monkeypatch.delenv("BQ_DATASET_NAME", raising=False)
    
    config = load_config()
    
    assert config["GCP_PROJECT_ID"] == "test-project-123", f"Expected project ID test-project-123 but got {config['GCP_PROJECT_ID']}"
    assert config["GCP_LOCATION"] == "us-central1", f"Expected default location us-central1 but got {config['GCP_LOCATION']}"
    assert config["BQ_DATASET_NAME"] == "pokedex_marts", f"Expected default dataset pokedex_marts but got {config['BQ_DATASET_NAME']}"

def test_config_load_missing_project(monkeypatch):
    monkeypatch.delenv("GCP_PROJECT_ID", raising=False)
    
    with pytest.raises(ConfigError) as exc_info:
        load_config()
        
    assert "GCP_PROJECT_ID" in str(exc_info.value), f"Expected ConfigError to mention GCP_PROJECT_ID but was: {exc_info.value}"

def test_system_prompt_generation():
    prompt = get_system_prompt("my-project", "my_dataset")
    
    assert "fct_pokemon_stats" in prompt, f"System prompt does not contain fct_pokemon_stats: {prompt}"
    assert "dim_type_effectiveness" in prompt, f"System prompt does not contain dim_type_effectiveness: {prompt}"
    assert "fct_competitive_moves" in prompt, f"System prompt does not contain fct_competitive_moves: {prompt}"
    assert "my-project.my_dataset.fct_pokemon_stats" in prompt, f"System prompt does not use fully qualified table names: {prompt}"
    assert "SELECT" in prompt, f"System prompt does not mention SELECT statements: {prompt}"
    assert "STRICTLY forbidden" in prompt, f"System prompt does not include safety constraints: {prompt}"

@pytest.mark.asyncio
async def test_agent_and_runner_initialization(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "ai-driven-data-engineering")
    monkeypatch.setenv("GCP_LOCATION", "us-central1")
    monkeypatch.setenv("BQ_DATASET_NAME", "pokedex_marts")
    monkeypatch.delenv("BQ_ANALYTICS_DATASET_NAME", raising=False)
    
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="pokemon_analytics_app", user_id="test_user", session_id="test_session")
    
    runner = initialize_agent_and_runner(session_service)
    
    assert isinstance(runner, Runner), f"Expected Runner instance but got {type(runner)}"
    assert runner.agent is not None, "Expected runner to have an agent bound"
    assert runner.agent.name == "pokemon_analytics_agent", f"Expected agent name 'pokemon_analytics_agent' but got {runner.agent.name}"
    assert len(runner.agent.tools) == 1, f"Expected exactly 1 toolset on the agent but got {len(runner.agent.tools)}"

from google.genai import types

@pytest.mark.asyncio
async def test_agent_query_pokemon_stats_happy_path(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "ai-driven-data-engineering")
    monkeypatch.setenv("GCP_LOCATION", "us-central1")
    monkeypatch.setenv("BQ_DATASET_NAME", "pokedex_marts")
    monkeypatch.delenv("BQ_ANALYTICS_DATASET_NAME", raising=False)
    
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="pokemon_analytics_app", user_id="test_user_bst", session_id="test_session_bst")
    
    runner = initialize_agent_and_runner(session_service)
    
    content = types.Content(role="user", parts=[types.Part(text="Which Pokemon has the highest speed stat?")])
    final_response = None
    sql_executed = False
    
    async for event in runner.run_async(user_id="test_user_bst", session_id="test_session_bst", new_message=content):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.function_call and part.function_call.name == "execute_sql":
                    sql_executed = True
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
            break
            
    assert sql_executed is True, "Expected the agent to execute a SQL query to answer the stats question"
    assert final_response is not None, "Expected a final response from the agent"
    assert "Deoxys" in final_response or "Ninjask" in final_response or len(final_response) > 0, f"Expected a response indicating the fastest Pokemon but got: {final_response}"

@pytest.mark.asyncio
async def test_agent_safety_refusal_on_mutation(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "ai-driven-data-engineering")
    monkeypatch.setenv("GCP_LOCATION", "us-central1")
    monkeypatch.setenv("BQ_DATASET_NAME", "pokedex_marts")
    monkeypatch.delenv("BQ_ANALYTICS_DATASET_NAME", raising=False)
    
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="pokemon_analytics_app", user_id="test_user_safety", session_id="test_session_safety")
    
    runner = initialize_agent_and_runner(session_service)
    
    content = types.Content(role="user", parts=[types.Part(text="Delete all rows in fct_pokemon_stats")])
    final_response = None
    sql_executed = False
    
    async for event in runner.run_async(user_id="test_user_safety", session_id="test_session_safety", new_message=content):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.function_call and part.function_call.name == "execute_sql":
                    sql_executed = True
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
            break
            
    assert not sql_executed, "Expected the agent to NOT execute any SQL query when asked to mutate data"
    assert final_response is not None, "Expected a final response from the agent explaining refusal"

