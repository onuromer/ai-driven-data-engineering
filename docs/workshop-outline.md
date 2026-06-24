# AI-Driven Data Engineering — Workshop Outline

## Overview

| | |
|---|---|
| **Title** | AI-Driven Data Engineering |
| **Duration** | 4–8 hours (single day, including breaks) |
| **Format** | In-person (adaptable to virtual/hybrid) |
| **Group Size** | 15–30 participants |
| **Staffing** | 1 lead instructor + helpers (~1 per 10 participants for groups >15) |
| **Language** | German (test run) / English (adaptable) |
| **Test Run** | University, ~2026-07-08 |

## Target Audience

**Experienced data engineers** (small business to enterprise) who want to learn how to use AI coding assistants effectively in their daily work.

- **What they know:** Data engineering — ingestion, transformation, modeling, orchestration, cloud platforms, SQL, Python
- **What they don't know:** Vibe coding, context engineering, working with AI coding assistants as a structured workflow
- **Core promise:** Move beyond "Prompt-and-Pray" to a reliable, repeatable AI-assisted development methodology for data engineering

## Data Source

**PokeAPI** (https://pokeapi.co/api/v2/)
- No authentication required — zero setup friction
- Rich, nested data model (Pokemon, types, abilities, stats, moves, evolution chains)
- Numeric stats ideal for BQML models in later labs
- Well-documented and familiar to AI tools — produces better vibe coding results
- Fun factor keeps energy up during an all-day workshop

## Tech Stack

| Layer | Tool | Notes |
|-------|------|-------|
| Ingestion | dlt (data load tool) | Open source, Python-native |
| Transformation | dbt | Open source, SQL-based |
| Local Database | DuckDB | Zero-config, runs anywhere |
| Cloud Database | BigQuery (GCP) | Production target |
| Infrastructure | Terraform | Cloud resource provisioning |
| Orchestration | Apache Airflow | Optional lab |
| Visualization | Streamlit | Optional lab |
| AI/ML | BQML + Gemini in BigQuery | Optional lab |

All core tools are **open source** — the workshop is platform-neutral by design, with GCP as one deployment target.

## AI Tools

Participants choose their preferred tool within each category:

| Category | Options |
|----------|---------|
| **CLI** | Claude Code, Antigravity CLI |
| **IDE** | Antigravity IDE (recommended), Cursor IDE (alternative) |

Lab instructions are written tool-agnostic where possible, with tool-specific setup notes where needed.

## MCP Servers

**Model Context Protocol (MCP)** servers extend AI tools with external knowledge and capabilities. The workshop uses **Context7** as a hands-on example:

- Provides up-to-date documentation for dlt, dbt, Airflow, Terraform, and other frameworks
- Bridges the gap between an AI model's training cutoff and the tools participants actually use
- Pre-configured in the starter project; covered conceptually in the intro slides
- Demonstrates a core context engineering principle: better context → better AI output

## AI Development Workflow

The workshop teaches a **skills-driven methodology** — a structured vibe coding workflow that makes AI reliable and repeatable:

```
create-prd → create-tasks → git-worktree → implement-tasks → finalize-tasks → document-learnings
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | `create-prd` | AI creates a Product Requirements Document through clarifying questions |
| 2 | `create-tasks` | AI breaks the PRD into vertical task slices |
| 3 | `git-worktree` | Isolated git branch per feature |
| 4 | `implement-tasks` | AI implements with tests, docs, and observability |
| 5 | `finalize-tasks` | Clean up worktree, resolve conflicts, create PR |
| 6 | `document-learnings` | Capture solutions as searchable knowledge |

This workflow is the **red thread** through the entire workshop. It is pre-configured in the starter project; the intro session explains the concepts, and each lab applies them.

---

## Schedule

### Intro — Foundations of AI-Driven Development (~60 min)

**Format:** Slides + live demo (delivered by instructor, not in this repo)

**Topics:**
1. The problem: "Prompt-and-Pray" vs. structured AI workflows
2. Context engineering: why context quality determines output quality
3. The AI development workflow: PRD → Tasks → Implement → Finalize → Learn
4. Project rules files: `CLAUDE.md`, `AGENTS.md`, `.cursorrules` — what they do and why
5. Skills: how agent skills enforce coding guidelines and standardize workflows
6. MCP servers: extending AI with external knowledge (Context7 as example)
7. Managing large data contexts: schemas, state files, complex data ecosystems
8. Tool overview: CLI tools (Claude Code, Antigravity CLI) vs. IDE tools (Antigravity IDE, Cursor)
9. Workshop setup: clone the starter repo, verify tool access

**By the end:** Participants understand the methodology, have the starter project cloned, and are ready for Lab 0.

---

### Lab 0 — Context Engineering & Project Planning (~60–75 min)

**Tool type:** CLI (Claude Code or Antigravity CLI)
**Environment:** Local
**Workflow focus:** `create-prd` → `create-tasks`

**What participants do:**
1. Explore the pre-configured starter project (CLAUDE.md, AGENTS.md, skills)
2. Use the `create-prd` skill to generate a PRD for the data project
   - Scope: data ingestion from PokeAPI + dbt transformation layers
   - The AI asks clarifying questions; participants guide the scope
3. Use the `create-tasks` skill to break the PRD into implementation tasks
4. Review and refine the generated PRD and task list

**What they learn:**
- How to structure a data engineering project so AI can act on it
- The difference between a vague prompt and a well-engineered PRD
- How task decomposition works when driven by AI
- The planning artifacts (PRD + tasks) that will guide Labs 1 and 2

**Checkpoints:**
- [ ] PRD file exists in `docs/prds/`
- [ ] Task file exists in `docs/tasks/`
- [ ] PRD covers PokeAPI ingestion + dbt transformation scope
- [ ] Tasks are broken into actionable, vertical slices

---

### Break (~15 min)

---

### Lab 1 — Data Ingestion with dlt (~60–75 min)

**Tool type:** CLI (Claude Code or Antigravity CLI)
**Environment:** Local (DuckDB)
**Workflow focus:** `git-worktree` → `implement-tasks` → `finalize-tasks`

**What participants do:**
1. Create a git worktree for the ingestion feature
2. Use `implement-tasks` to have AI build a dlt pipeline:
   - Source: PokeAPI REST endpoints (pokemon, types, abilities, moves, stats)
   - Destination: Local DuckDB (`data/pokedex.db`)
   - Incremental loading strategy with `write_disposition="merge"`
   - Schema evolution for nested JSON data
3. Run the pipeline and verify data in DuckDB
4. Use `finalize-tasks` to clean up and create a PR

**What they learn:**
- How AI handles REST API ingestion code generation
- Managing complex/nested schemas through context engineering
- The implement → test → finalize cycle in practice
- How dlt works (for those unfamiliar)

**Checkpoints:**
- [ ] dlt pipeline runs successfully
- [ ] Data loaded into DuckDB with correct schema
- [ ] Nested data (stats, types) handled properly
- [ ] Tests pass
- [ ] PR created via `finalize-tasks`

---

### Lunch Break (~45–60 min)

---

### Lab 2 — Data Transformation with dbt (~60–75 min)

**Tool type:** IDE (Antigravity IDE recommended, Cursor as alternative)
**Environment:** Local (DuckDB)
**Workflow focus:** `git-worktree` → `implement-tasks` → `finalize-tasks`

**What participants do:**
1. Switch to an IDE tool — experience the difference from CLI
2. Create a git worktree for the transformation feature
3. Use `implement-tasks` to have AI build dbt models:
   - **Staging layer:** Clean, typed, 1:1 mapping of raw dlt tables
   - **Marts layer:** Analytical models with joins and aggregations
     - `fct_pokemon_stats` — base stats with BST (Base Stat Total)
     - `dim_type_effectiveness` — type matchup matrix
     - `fct_competitive_moves` — moves with STAB calculation
4. Run `dbt build` and verify models
5. Use `finalize-tasks` to clean up and create a PR

**What they learn:**
- How the same workflow applies in an IDE context
- AI-assisted SQL modeling and dbt project structure
- Medallion architecture (raw → staging → marts) through vibe coding
- How AI handles complex SQL logic (window functions, STAB calculations)

**Checkpoints:**
- [ ] dbt project structure created (`transform/`)
- [ ] Staging models pass `dbt build`
- [ ] Mart models with joins and calculations pass
- [ ] dbt tests (uniqueness, not-null, relationships) pass
- [ ] PR created via `finalize-tasks`

---

### Break (~15 min)

---

### Lab 3 — Go to Cloud (~60–75 min)

**Tool type:** IDE (Antigravity IDE recommended, Cursor as alternative)
**Environment:** Local + GCP Playground
**Workflow focus:** `create-prd` (update) → `create-tasks` → `implement-tasks` → `finalize-tasks`

**What participants do:**
1. **Requirements change!** — Update the PRD with cloud requirements:
   - Deploy infrastructure to GCP using Terraform
   - Switch pipeline destination from DuckDB to BigQuery
   - Adapt dbt to target BigQuery
2. Generate new tasks from the updated PRD
3. Use AI to generate Terraform files:
   - BigQuery dataset(s)
   - GCS bucket (for dlt staging)
   - IAM / service account configuration
4. Apply Terraform against the GCP Playground
5. Adapt the dlt pipeline to target BigQuery instead of DuckDB
6. Adapt dbt to run against BigQuery
7. Run the full pipeline end-to-end on GCP

**What they learn:**
- How to evolve a project when requirements change (update PRD → re-plan → implement)
- AI-assisted Infrastructure-as-Code (Terraform/HCL generation)
- The local → cloud transition pattern
- How context engineering scales beyond application code to infrastructure

**Checkpoints:**
- [ ] PRD updated with cloud requirements
- [ ] New tasks generated
- [ ] Terraform files created and applied to GCP
- [ ] dlt pipeline loads data into BigQuery
- [ ] dbt models run against BigQuery
- [ ] PR created via `finalize-tasks`

---

### Optional Labs (~60–75 min each)

For faster groups, extended workshop formats, or take-home exercises.

#### Lab 4a — Orchestration with Airflow

**Environment:** GCP
**What participants build:** An Airflow DAG that orchestrates the full pipeline (dlt ingestion → dbt transformation) on a schedule.

#### Lab 4b — Visualization with Streamlit

**Environment:** Local or GCP
**What participants build:** A Streamlit dashboard visualizing the mart layer — Pokemon power rankings, type effectiveness heatmap, move pool analytics.

#### Lab 4c — AI/ML on BigQuery

**Environment:** GCP
**What participants build:**
- **BQML:** Train a classification model to predict Pokemon type from base stats
- **Gemini in BigQuery:** Use `ML.GENERATE_TEXT` to generate natural-language scouting reports from structured Pokemon data

---

## What Participants Receive

### Before the Workshop
- **Setup guide:** Install Python 3.11+, dlt, dbt, DuckDB, git, and their chosen AI tool (Claude Code / Antigravity CLI / Antigravity IDE / Cursor)
- **Repo access:** Clone the starter project

### At the Workshop
- **GCP Playground:** Pre-provisioned GCP project with BigQuery, GCS, and necessary APIs enabled
- **AI model access:** API keys for vibe coding tools (provided by Google)

### From the Repo
- **Starter project:** Pre-configured `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, skills workflow, base `requirements.txt`
- **Lab instructions:** README per lab with learning objectives, prompts, and checkpoints
- **Reference solutions:** Complete working code per lab for catch-up and validation

---

## Repo Structure

```
ai-driven-data-engineering/
│
├── docs/                              # Workshop planning (not participant-facing)
│   ├── brainstorming.md
│   └── workshop-outline.md            # This file
│
├── labs/
│   ├── lab_0_context_engineering/
│   │   ├── README.md                  # Instructions, objectives, checkpoints
│   │   ├── prompts/                   # Prompts for PRD + task creation
│   │   └── solutions/                 # Reference PRD, task files
│   │
│   ├── lab_1_ingestion/
│   │   ├── README.md
│   │   ├── prompts/
│   │   └── solutions/                 # Reference dlt pipeline
│   │
│   ├── lab_2_transformation/
│   │   ├── README.md
│   │   ├── prompts/
│   │   └── solutions/                 # Reference dbt project
│   │
│   ├── lab_3_cloud/
│   │   ├── README.md
│   │   ├── prompts/
│   │   └── solutions/                 # Reference Terraform + adapted pipeline
│   │
│   ├── lab_4a_orchestration/          # Optional
│   │   ├── README.md
│   │   ├── prompts/
│   │   └── solutions/
│   │
│   ├── lab_4b_visualization/          # Optional
│   │   ├── README.md
│   │   ├── prompts/
│   │   └── solutions/
│   │
│   └── lab_4c_ai_ml/                  # Optional
│       ├── README.md
│       ├── prompts/
│       └── solutions/
│
├── starter/                           # What participants clone and work in
│   ├── AGENTS.md                      # Shared agent instructions (all tools)
│   ├── CLAUDE.md                      # Claude Code project rules
│   ├── GEMINI.md                      # Antigravity CLI project rules
│   ├── .cursorrules                   # Cursor IDE project rules
│   ├── .agents/skills/                # Full skills workflow
│   ├── .claude/settings.json          # MCP config (Context7) — Claude Code
│   ├── .gemini/settings.json          # MCP config (Context7) — Antigravity CLI
│   ├── .geminiignore                  # Antigravity CLI file exclusions
│   ├── requirements.txt
│   └── README.md                      # "Start here"
│
├── CLAUDE.md                          # Repo-level (for workshop development)
├── AGENTS.md
├── .gitignore
└── LICENSE
```

---

## Key Design Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | OSS-first stack (dlt, dbt, Airflow) | Platform-neutral — skills transfer to any cloud or on-prem |
| 2 | Tool category per lab, not brand | Participants choose their tool; instructions stay portable |
| 3 | Local → Cloud progression | Reduces setup friction early; mirrors real dev workflows |
| 4 | Skills pre-configured in starter | Maximizes hands-on time; intro slides cover the concepts |
| 5 | PRD created in Lab 0, updated in Lab 3 | Teaches both greenfield planning and requirement evolution |
| 6 | PokeAPI as data source | Fun, no auth, rich data, AI tools know it well, great for BQML |
| 7 | Progressive build across labs | Each lab adds a layer; final result is a full data platform |
| 8 | Reference solutions per lab | Safety net for participants who fall behind; validation for authors |
