# Prompt: Create PRD for the Dashboard

Copy the prompt below into your AI coding assistant.

~~~
Act as a Senior Full-Stack Data Engineer. Create a Product Requirements Document (PRD) for a data visualization dashboard.

Use skill: create-prd

Important: The scope below is already well-defined. Only ask clarifying questions about areas that are genuinely ambiguous or missing. If everything is clear, proceed directly to generating the PRD.

FEATURE SCOPE

Build a multi-tab Streamlit web application to visualize the mart-layer insights for competitive Pokemon analytics.

- Backend: Connect to the local DuckDB database at data/pokedex.db using the duckdb Python library
- Do NOT support BigQuery — keep it DuckDB-only for simplicity
- Location: All application code in the app/ directory

DASHBOARD TABS

1. Power Rankings — Searchable/filterable table of Pokemon with Base Stat Total (BST), sortable by any stat. Radar chart to compare stats of two selected Pokemon side by side (use st.selectbox for selection).

2. Type Synergy & Counters — Heatmap visualization of the type effectiveness matrix from dim_type_effectiveness (18x18 grid, color-coded by damage_multiplier). Interactive tool: select an opponent's Pokemon type (not individual Pokemon) from a dropdown, and show which attacking types are super effective (damage_multiplier = 2.0) against it.

3. Move Pool Analytics — Scatter plot of move power (x-axis) vs accuracy (y-axis), colored by damage_class (physical/special/status). Table of top 10 highest STAB-adjusted damage dealers from fct_competitive_moves, grouped by move_type.

SIDEBAR FILTERS

- Primary type dropdown (filters Power Rankings and Move Pool tabs)
- Do NOT include a generation filter — the data doesn't have a generation column in fct_pokemon_stats
- Filters persist across tabs using st.session_state

TECHNICAL REQUIREMENTS

- Use duckdb Python library to query mart tables directly (marts.fct_pokemon_stats, marts.dim_type_effectiveness, marts.fct_competitive_moves)
- Use plotly for all interactive charts (radar, heatmap, scatter)
- Use st.dataframe for tables
- Design: Use Streamlit's default theme, no custom CSS needed. Keep it clean and functional.
- Project structure:
  - app/main.py — Entry point (tab navigation, sidebar, page config)
  - app/utils.py — Database connection and SQL query functions
  - app/visuals.py — Chart generation functions (plotly figures)

DEPENDENCIES

Add to requirements.txt: streamlit, plotly, duckdb
~~~
