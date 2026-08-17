# CloudIntel — Enterprise AI FinOps Platform

CloudIntel is an enterprise-grade AI FinOps intelligence platform designed to eliminate cloud waste across decentralized Business Units (BUs) while strictly enforcing financial institution security, KMS encryption mandates, and compliance guardrails.

---

## Key Features

- **Multi-Service Focus (Phase 1 POC)**: Ingests & analyzes **Amazon ECS (EC2 launch type)** container workloads, **AWS Lambda** serverless compute, and **Amazon S3** object storage.
- **100% Free / Lightweight POC Stack**:
  - **Groq Cloud API** (`llama-3.3-70b-versatile`) — High-speed LPU inference engine.
  - **DuckDB** (`data/processed/cloudintel.duckdb`) — In-process columnar OLAP analytical database.
  - **Streamlit Web UI** — Interactive multi-tab web application.
- **Banking Security & Compliance Guardrails Engine**: Intercepts candidate recommendations before presentation to ensure KMS keys are never deleted, security sidecars are preserved, and public access blocks are enforced.
- **AWS CloudFormation & Service Catalog Studio**: Auto-generates compliant AWS CloudFormation YAML templates and AWS Service Catalog Product definition metadata JSON.

---

## Repository Structure

```plaintext
cloudintel/
├── data/
│   ├── raw/                      # Raw billing CSVs, ECS task metrics, Lambda & S3 stats
│   │   ├── aws_cur_export.csv
│   │   ├── ecs_task_metrics.json
│   │   ├── lambda_metrics.json
│   │   └── s3_storage_metrics.json
│   └── processed/                # Cleaned analytical DuckDB database
│       └── cloudintel.duckdb
├── docs/                         # Specification & architecture documentation
│   ├── PROBLEM_STATEMENT.md      # Problem statement & milestone scope
│   ├── ARCHITECTURE.md           # System architecture specification
│   ├── Implementation-plan.md   # Week-by-week technical implementation roadmap
│   ├── deployment-plan.md       # Operational deployment guide (POC to Production)
│   └── edge-case.md              # Corner scenarios & risk mitigation specification
├── tests/                        # Automated unit test suite
│   ├── test_guardrails.py
│   └── test_sql_safety.py
├── ingest.py                     # Week 1: Multi-service ETL & DuckDB ingestion engine
├── query_agent.py                # Week 2: Text-to-SQL & context synthesis agent
├── analyzer.py                   # Week 3: Proactive multi-service waste analyzer
├── guardrails.py                 # Week 3: Banking Security & Compliance Policy Engine
├── iac_generator.py              # Week 4: Compliant CloudFormation & Service Catalog generator
├── app.py                        # Week 4: Streamlit interactive web application
├── llm_client.py                 # Pluggable LLM provider client (Groq / Fallback)
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation & quickstart guide
```

---

## Quickstart Guide

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# Activate virtual environment (Linux/macOS)
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional for Groq API)
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=gsk_your_groq_api_key_here
LLM_MODEL_NAME=llama-3.3-70b-versatile
GUARDRAILS_MODE=ENFORCE
```
*(Note: CloudIntel includes a built-in heuristic fallback engine, allowing offline testing even if `GROQ_API_KEY` is omitted).*

### 3. Run Data Ingestion Pipeline (ETL)
```bash
python ingest.py
```

### 4. Run Proactive Waste Analyzer & Guardrails Interceptor
```bash
python analyzer.py
```

### 5. Launch Streamlit Portal Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## Automated Unit Testing

Run the automated test suite covering AST SQL safety checks and banking guardrail enforcement:
```bash
python -m unittest discover tests
```

---

## Architectural Data Flow

```
Raw CUR Billing CSV & Resource Logs (ECS, Lambda, S3)
  ↓
Data Ingestion Pipeline (ingest.py) → DuckDB (cloudintel.duckdb)
  ↓
Natural Language Q&A (query_agent.py) ↔ Text-to-SQL (Groq API)
  ↓
Proactive Waste Analyzer (analyzer.py)
  ↓
Banking Compliance Guardrails (guardrails.py) → Intercept Unsafe Fixes (e.g. KMS Deletion)
  ↓
Remediation Engine (iac_generator.py) → CloudFormation YAML + Service Catalog JSON
  ↓
Streamlit UI Application (app.py)
```
