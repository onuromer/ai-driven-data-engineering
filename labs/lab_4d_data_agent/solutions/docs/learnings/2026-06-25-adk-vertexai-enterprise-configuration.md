# Learning: ADK Vertex AI Enterprise Configuration

## Problem
When initializing a Python-based agent using the Google Agent Development Kit (ADK) on a Google Cloud Platform Compute Engine or similar VM, the GenAI client may throw a `ValueError: No API key was provided.` or a `ClientError: 403 PERMISSION_DENIED` because the Agent Platform API was not enabled or the client default backend tried to query the public Gemini developer API.

## Solution

1. **Vertex AI API Enablement**:
   Ensure that the Vertex AI Agent Platform API is enabled in the target Google Cloud project:
   ```bash
   gcloud services enable aiplatform.googleapis.com --project=YOUR_PROJECT_ID
   ```

2. **Vertex AI Backend Integration**:
   Set `GOOGLE_GENAI_USE_ENTERPRISE = 'True'` in the environment variables before instantiating the model or runner. This instructs the underlying `google-genai` library client to use the Vertex AI endpoint backend instead of the public Gemini developer backend, leveraging Google Application Default Credentials (ADC) for authentication.
   
   In Python:
   ```python
   import os
   
   os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
   os.environ['GOOGLE_CLOUD_LOCATION'] = location
   os.environ['GOOGLE_GENAI_USE_ENTERPRISE'] = 'True'
   ```

## References
- Google ADK SDK documentation: [google-adk.txt](file:///Users/saschadi/GitHub/ai-driven-data-engineering/tmp/starter-4d/docs/knowledge/google-adk.txt)
- [agent.py](file:///Users/saschadi/GitHub/ai-driven-data-engineering/tmp/starter-4d/agent/agent.py)
