# Lab 4c — AI/ML on It: BQML & Gemini on BigQuery

*Optional lab — for faster groups, extended workshops, or take-home exercise.*

In this lab you'll use AI to create machine learning models and generative AI queries directly in BigQuery — no separate ML infrastructure needed. Train a BQML classification model to predict Pokemon types from stats, and use Gemini to generate natural-language scouting reports from structured data.

## Learning Objectives

- Use AI coding assistants to generate BQML training queries
- Train a classification model directly in BigQuery
- Use Gemini's `ML.GENERATE_TEXT` function within SQL queries
- See how AI handles ML-specific code generation

## Tools

| | |
|---|---|
| **Tool type** | CLI or IDE (your choice) |
| **Environment** | GCP (BigQuery) |
| **Duration** | 60–75 minutes |

## Prerequisites

- Lab 3 completed (data available in BigQuery)
- GCP Playground with Gemini API enabled

## Steps

### Step 1 — Create a PRD for AI/ML Features (10 min)

1. Copy the prompt from [`prompts/01_create_prd.md`](prompts/01_create_prd.md) into your AI assistant
2. Answer clarifying questions based on the prompt guidance
3. Review the generated PRD

### Step 2 — Create Tasks and Implement (40–50 min)

1. Use `create-tasks` to generate task breakdowns
2. Create a feature branch with `git-worktree`
3. Use `implement-tasks` with the prompt from [`prompts/02_implement_ai_ml.md`](prompts/02_implement_ai_ml.md)
4. The AI should create:
   - BQML model training SQL (classification: predict type from stats)
   - BQML evaluation and prediction queries
   - Gemini-powered scouting report query

### Step 3 — Run and Validate (10–15 min)

1. Execute the BQML training query in BigQuery
2. Evaluate model accuracy
3. Run a prediction query on new Pokemon
4. Run the Gemini scouting report query
5. Use `finalize-tasks` to create a PR

## Checkpoints

- [ ] PRD for AI/ML feature exists
- [ ] BQML classification model created in BigQuery
- [ ] Model evaluation shows reasonable accuracy
- [ ] Prediction query works on sample Pokemon
- [ ] Gemini `ML.GENERATE_TEXT` query generates scouting reports
- [ ] SQL files or dbt models for all queries exist in the project
- [ ] PR created

## Next

Try another optional lab:
- [Lab 4a — Orchestrate It](../lab_4a_orchestration/README.md)
- [Lab 4b — Visualize It](../lab_4b_visualization/README.md)
