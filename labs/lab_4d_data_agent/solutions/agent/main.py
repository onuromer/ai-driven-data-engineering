import os
import sys
from pathlib import Path

# Fix import path when running main.py directly
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))
if str(current_dir) in sys.path:
    sys.path.remove(str(current_dir))

import asyncio
import logging
from google.genai import types
from google.adk.sessions import InMemorySessionService

from agent.agent import initialize_agent_and_runner
from agent.config import ConfigError

# Configure logging
logging.basicConfig(
    level=logging.WARNING, # Keep stdout/stderr clean from diagnostic logs by default
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("pokemon_agent.main")

async def run_query(query: str, runner, user_id: str, session_id: str):
    """
    Sends a query to the agent, intercepts executed SQL queries, 
    and prints the final agent response.
    """
    # Prepare the user message in ADK Content format
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    final_response_text = "Agent did not produce a final response."
    
    try:
        # Run conversation turn asynchronously and process events
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            # Intercept BQ SQL execution tool calls
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.function_call and part.function_call.name == "execute_sql":
                        sql_query = part.function_call.args.get("query")
                        if sql_query:
                            print(f"\n[SQL Query Executed]:\n{sql_query.strip()}\n")
            
            # Check for final response
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                break
                
    except Exception as e:
        logger.error(f"Error executing agent query: {e}", exc_info=True)
        print(f"\n[Error]: Failed to process query. Detail: {e}")
        return
        
    print(f"[Agent Response]:\n{final_response_text}\n")

async def main():
    # Verify environment and configuration
    try:
        session_service = InMemorySessionService()
        
        # Setup conversation session
        app_name = "pokemon_analytics_app"
        user_id = "default_user"
        session_id = "default_session"
        
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        # Initialize Runner
        runner = initialize_agent_and_runner(session_service)
        
    except ConfigError as ce:
        print(f"Configuration Error: {ce}", file=sys.stderr)
        print("Please check your environment variables (e.g. GCP_PROJECT_ID, GCP_LOCATION).", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Initialization Failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("=== Pokemon Analytics Conversational Data Agent ===")
    print("Ask questions about stats, type effectiveness, or moves.")
    print("Type 'exit' or 'quit' to end the session.")
    print("=" * 60)

    # Interactive input loop
    while True:
        try:
            # Python's input() is synchronous, so we run it in an executor to avoid blocking the async event loop
            loop = asyncio.get_running_loop()
            user_query = await loop.run_in_executor(None, lambda: input(">>> Ask Pokemon Agent: "))
            
            if user_query.strip().lower() in ["exit", "quit"]:
                print("Exiting Pokemon Agent. Goodbye!")
                break
                
            if not user_query.strip():
                continue
                
            await run_query(user_query, runner, user_id, session_id)
            
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Pokemon Agent. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred in the conversation loop: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
