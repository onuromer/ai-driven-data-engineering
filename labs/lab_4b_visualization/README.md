# Lab 4b — Visualize It: Streamlit Dashboard

*Optional lab — for faster groups, extended workshops, or take-home exercise.*

In this lab you'll have AI build a Streamlit dashboard that visualizes the analytical models from Lab 2. Power rankings, type effectiveness heatmaps, and move pool analytics — all driven by the data you've already modeled.

## Learning Objectives

- Use the full AI workflow cycle for a frontend/visualization feature
- See how AI generates interactive data applications
- Connect a Streamlit app to DuckDB or BigQuery

## Tools

| | |
|---|---|
| **Tool type** | CLI or IDE (your choice) |
| **Environment** | Local (DuckDB) or GCP (BigQuery) |
| **Duration** | 60–75 minutes |

## Prerequisites

- Lab 2 completed (dbt mart models exist in DuckDB)
- Or Lab 3 completed (mart models in BigQuery)

## Steps

### Step 1 — Create a PRD for the Dashboard (10 min)

1. Copy the prompt from [`prompts/01_create_prd.md`](prompts/01_create_prd.md) into your AI assistant
2. Answer clarifying questions based on the prompt guidance
3. Review the generated PRD

### Step 2 — Create Tasks and Implement (40–50 min)

1. Use `create-tasks` to generate task breakdowns
2. Create a feature branch with `git-worktree`
3. Use `implement-tasks` with the prompt from [`prompts/02_implement_visualization.md`](prompts/02_implement_visualization.md)
4. The AI should create a multi-tab Streamlit app with:
   - Power Rankings tab (searchable stats table, radar chart comparisons)
   - Type Synergy tab (heatmap of type effectiveness matrix)
   - Move Pool tab (move distribution charts, STAB damage dealers)

### Step 3 — Run and Test (10–15 min)

1. Start the Streamlit app:
   ```bash
   uv run streamlit run app/main.py
   ```
2. Interact with the dashboard — do filters work? Are charts meaningful?
3. Document what you learned:
   ```
   Use skill: document-learnings
   ```
4. Use `finalize-tasks` to create a PR

## Checkpoints

- [ ] PRD for visualization feature exists
- [ ] Streamlit app created in `app/` directory
- [ ] Dashboard connects to DuckDB (or BigQuery) and queries mart models
- [ ] At least 2 tabs with interactive charts
- [ ] App runs without errors
- [ ] PR created

## Next

Try another optional lab:
- [Lab 4a — Orchestrate It](../lab_4a_orchestration/README.md)
- [Lab 4c — AI/ML on It](../lab_4c_ai_ml/README.md)
