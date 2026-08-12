Project: CloudIntel — Enterprise AI FinOps Platform
The Big Problem
Every enterprise cloud strategy fails the same way financially: cloud consumption is decentralized across multiple Business Units (BUs), leading to massive, untracked waste (often 20-35% of total spend). Information is siloed. Existing cloud management tools are highly technical, throwing JSON logs and complex graphs at business stakeholders who just want to know, "Why did our bill spike yesterday?" Furthermore, when one BU solves a complex cost optimization problem, that knowledge never transfers to other BUs.

Goal: Build an end-to-end Enterprise AI Platform powered by an advanced Large Language Model (like Claude). The system must ingest raw cloud billing and usage data, translate natural language questions from business stakeholders into complex cloud queries, perform multi-dimensional reasoning to spot cross-BU waste patterns, and automatically generate compliant Infrastructure as Code (IaC) to remediate the issues.

Not just a dashboard. Not a generic code copilot. A contextual FinOps intelligence engine that speaks business logic and writes infrastructure code.

Final System (What you're building over 4 weeks)
Ingest Cloud Cost & Usage Reports (CUR), Metrics, and Logs
↓
AI translates natural language into complex data queries
↓
AI analyzes multi-dimensional patterns (cost + performance + business hours)
↓
AI auto-generates proactive insights & custom IaC (Terraform) remediation
↓
Business & Engineering query it via an interactive chat interface
↓
Deployed as an enterprise-wide FinOps application

Week-by-Week Problem Statements
Each week is a self-contained problem. Build it, test it on real, anonymized cloud billing/usage data, and use each week's output as the foundation for the next.

Week 1 — The Data Pipeline: "Ingest the Cloud"
Problem
Cloud billing data is massive, granular, and hard to parse. You need a centralized pipeline to capture Cost & Usage Reports (CUR) and resource metrics so the AI has a factual foundation to query against.

Build

Set up the project structure from scratch:

data/raw/ — where raw cloud billing exports (CSV/JSON) land.

data/processed/ — cleaned, aggregated data ready for querying.

Write a Python ingestion script that:

Reads raw cost data and resource logs (e.g., EC2 usage, S3 buckets).

Normalizes the data into a standard schema (Resource ID, BU Tag, Daily Cost, Usage Metric).

Stores it in a lightweight local database (SQLite/DuckDB) for fast querying.

Test it on a sample dataset of real cloud logs representing at least 3 distinct "Business Units."

Deliverable ("Ship the Ingestion Engine")
A working data pipeline—one command cleans and loads raw cloud logs into a structured, queryable database.
🏅 Badge: The Cloud Data Architect

Acceptance Criteria

data/raw/ and data/processed/ structure exists.

Script successfully parses CSV/JSON billing exports.

Data is standardized into a queryable local database.

Contains mocked or anonymized data for at least 3 distinct BUs.

Week 2 — The Translator: "Speak Business, Query Cloud"
Problem
Business leaders ask questions like, "Why did the marketing app cost so much last week?" Existing tools require SQL or complex dashboard filters to answer this. You need the AI to translate human intent into precise database queries.

Build

2.1 — Intent Parsing (The NLP Layer)

Write a function that passes a user's plain-English question to the LLM (e.g., Claude API).

Instruct the LLM to translate the question into a valid SQL query against your local cost database.

2.2 — Context Synthesis (The Explainer)

Execute the AI-generated SQL query.

Feed the raw data results back to the LLM so it can generate a human-readable, business-contextual answer (e.g., "The spike was caused by an EMR cluster left running over the weekend by the data team.")

Deliverable ("Ship the Natural Language FinOps Agent")
A pipeline that takes a plain-English question, writes the query, fetches the data, and returns a contextual answer.
🏅 Badge: The Translator

Acceptance Criteria

Natural language input successfully maps to executable SQL.

Queries execute against the database from Week 1 without errors.

System returns a plain-text, contextual explanation of the costs.

Tested successfully on 10+ varied business questions.

Week 3 — The Intelligence Engine: "Find the Hidden Waste"
Problem
Reactive Q&A is good, but proactive optimization is better. The system needs to analyze the data autonomously for the 7 major waste categories (Compute, Storage, Database, Network, Serverless, Non-business hours, Logging) using multi-dimensional reasoning.

Build

3.1 — Pattern Recognition Logic

Write an analysis script that feeds resource metrics to the LLM and asks it to identify inefficiencies (e.g., a high-throughput stream running 24/7 when business hours are only 9-5).

3.2 — Cross-BU Learning

Implement logic where the LLM scans for identical architectural patterns across different BUs. If BU 'A' has unattached storage volumes, the LLM flags similar unattached volumes in BU 'B'.

Deliverable ("Ship the Proactive Analyst")
An automated job that scans the database, identifies complex optimization opportunities, and flags them with estimated savings.
🏅 Badge: The Cost Detective

Acceptance Criteria

Script successfully identifies at least 3 different categories of waste (e.g., idle compute, unattached storage).

LLM provides reasoning for why it is waste based on usage patterns.

System identifies a shared inefficiency across two different BUs.

Week 4 — The Fixer: "Ask, Analyze, Automate"
Problem
Identifying waste is only half the battle; engineering teams need the actual code to fix it. You need to wire the intelligence engine to an Infrastructure as Code (IaC) generator and package it into a clean UI.

Build

4.1 — The Remediation Engine

Extend the LLM prompt: When a cost optimization is approved, instruct the LLM to generate the exact, company-compliant Terraform or Python (Boto3) script to remediate the issue (e.g., auto-scale a database, delete stale snapshots).

4.2 — UI & Deployment

Assemble everything into a Streamlit app:

A chat interface for Q&A.

A dashboard of proactive cost-saving recommendations.

A "Generate Fix" button that outputs the required IaC.

Deploy to a platform (Streamlit Cloud / internal host).

Deliverable ("Ship CloudIntel" — the final product)
Deploy the complete system—data ingestion → natural language Q&A → proactive waste detection → IaC generation—all wired into one Streamlit app.
🏅 Badge: The Automation Oracle

Acceptance Criteria

LLM successfully generates valid Terraform/Python remediation scripts based on the identified waste.

One Streamlit app contains both the search/chat bar and the proactive recommendations.

Deployed live and accessible via URL.

Full pipeline works end-to-end.

Final Deliverables (Whole Project)
Public/Internal repo with a clean README.md + setup instructions.

Live deployed URL — interactive chat + actionable cost recommendations.

End-to-end flow verified: ingest → query → analyze → generate IaC.

All 4 weekly milestones complete.

Suggested Repo Structure
Plaintext
cloudintel/
├── data/
│   ├── raw/              # Week 1: Raw cloud cost exports
│   └── processed/        # Week 1: Cleaned SQLite/DuckDB database
├── ingest.py             # Week 1: ETL script for cloud logs
├── query_agent.py        # Week 2: LLM SQL generation and synthesis
├── analyzer.py           # Week 3: Proactive waste pattern recognition
├── iac_generator.py      # Week 4: Terraform/Python remediation generation
├── app.py                # Week 4: Streamlit UI (Chat + Insights)
├── requirements.txt
└── README.md
Suggested Build Order
Scaffold repo structure + requirements.txt

ingest.py → test on raw CSV/JSON data to populate database (Week 1)

query_agent.py → test text-to-SQL and answer synthesis (Week 2)

analyzer.py → run multi-dimensional reasoning prompts (Week 3)

iac_generator.py → test Terraform generation based on insights (Week 4.1)

app.py → Streamlit app combining chat, insights, and code generation (Week 4.2)

Deploy app → test end-to-end workflow

Write README.md, finalize documentation