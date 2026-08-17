# Deployment Plan — CloudIntel: Enterprise AI FinOps Platform

## Executive Summary & Vision

This document details the deployment operational plan for **CloudIntel**, an enterprise-grade AI FinOps intelligence platform. It outlines the step-by-step procedure for deploying, configuring, hosting, operating, and promoting CloudIntel across environments—from **Phase 1 (Proof of Concept Local/Sandbox Deployment)** to **Phase 2 (Enterprise Banking Cloud Production)**.

This plan integrates requirements from [`docs/PROBLEM_STATEMENT.md`](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/PROBLEM_STATEMENT.md), [`docs/ARCHITECTURE.md`](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/ARCHITECTURE.md), and [`docs/Implementation-plan.md`](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/Implementation-plan.md).

---

## Deployment Strategy & Two-Phase Model

CloudIntel deployment is structured in two sequential phases to guarantee zero initial cloud infrastructure cost, zero risk to live workloads, and complete validation before enterprise rollout:

```
[ Phase 1: POC Local / Sandbox ]
  ├── Embedded DuckDB OLAP
  ├── Groq LPU API (llama-3.3-70b-versatile)
  ├── Local Streamlit Portal (Port 8501)
  └── Local File Ingestion (data/raw -> data/processed)
           │
           ▼ (Validation & Stakeholder Approval)
[ Phase 2: Enterprise Cloud Production ]
  ├── AWS Athena / Redshift + AWS S3 Data Lake
  ├── Anthropic Claude 3.5 Sonnet (Enterprise License)
  ├── AWS App Runner / ECS Fargate + ALB + Banking SSO (OIDC/SAML)
  └── AWS Service Catalog Portfolio Pipeline Integration
```

---

## Environment Matrix & Prerequisites

### 1. Phase 1 (POC Sandbox Environment)

| Requirement | Specification |
| :--- | :--- |
| **Operating System** | Linux / macOS / Windows 10+ (PowerShell or Bash) |
| **Runtime Environment** | Python 3.10+ |
| **Package Manager** | `pip` with virtual environment (`venv`) |
| **System Memory** | Minimum 4 GB RAM (8 GB recommended for DuckDB in-memory aggregations) |
| **Storage** | 1 GB free disk space for raw logs and DuckDB database file |
| **External Connectivity** | HTTPS outbound access to `api.groq.com` (Port 443) |

### 2. Phase 2 (Enterprise Banking Cloud Target)

| Component | Target AWS Service / Architecture |
| :--- | :--- |
| **Application Hosting** | **AWS App Runner** or **Amazon ECS Fargate** (Private Subnets) |
| **Load Balancing & Auth** | **AWS ALB** + AWS IAM / Banking SSO (OIDC / SAML 2.0) |
| **Analytical Query Engine**| **AWS Athena** / **Amazon Redshift Serverless** |
| **Data Lake Storage** | **AWS S3 Bucket** + **AWS Glue Data Catalog** |
| **Secrets & Keys** | **AWS Secrets Manager** + **AWS KMS (Customer Managed Keys)** |
| **IaC Delivery Target** | **AWS Service Catalog** Product Portfolios via AWS CodePipeline |

---

## Configuration & Environment Variables

Create a `.env` file in the project root directory (ensure `.env` is listed in `.gitignore`):

```bash
# Core Application Environment
APP_ENV=development
LOG_LEVEL=INFO

# Phase 1 LLM Provider Configuration
GROQ_API_KEY=gsk_your_groq_api_key_here
LLM_MODEL_NAME=llama-3.3-70b-versatile

# Phase 2 LLM Provider Configuration (Target)
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# LLM_MODEL_NAME=claude-3-5-sonnet-20241022

# Database & Storage Settings
DUCKDB_PATH=data/processed/cloudintel.duckdb
DATA_RAW_DIR=data/raw

# Banking Compliance Guardrails Toggle (ENFORCE | AUDIT)
GUARDRAILS_MODE=ENFORCE
ENFORCE_KMS_MANDATE=true
ENFORCE_ECS_SIDECARS=true
ENFORCE_LAMBDA_MEMORY_BOUNDS=true
ENFORCE_ZERO_PUBLIC_ACCESS=true
```

---

## Step-by-Step Phase 1 (POC) Deployment Guide

### Step 1: Repository Clone & Workspace Setup
```bash
git clone https://github.com/your-org/cloudintel.git
cd cloudintel
```

### Step 2: Virtual Environment & Dependency Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# Activate virtual environment (Linux/macOS)
# source venv/bin/activate

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Raw Data Provisioning
Ensure mock billing data and multi-service metric logs are present in `data/raw/`:
- `data/raw/aws_cur_export.csv`
- `data/raw/ecs_task_metrics.json`
- `data/raw/lambda_metrics.json`
- `data/raw/s3_storage_metrics.json`

### Step 4: Run Data Ingestion Pipeline (ETL & DuckDB Load)
```bash
python ingest.py
```
*Expected Output*:
- Cleans and normalizes multi-service cost and usage metrics.
- Populates `data/processed/cloudintel.duckdb`.
- Displays record counts for `raw_cost_reports`, `ecs_task_metrics`, `lambda_metrics`, and `s3_storage_metrics`.

### Step 5: Run Waste Analyzer & Guardrails Verification
```bash
python analyzer.py
```
*Expected Output*:
- Evaluates ECS task reservations, Lambda memory utilization, and S3 object storage age.
- Intercepts candidates via `guardrails.py`.
- Populates `candidate_recommendations` table in DuckDB with `APPROVED` or `REJECTED_*` flags.

### Step 6: Launch Streamlit Web UI Application
```bash
streamlit run app.py --server.port 8501 --server.address 127.0.0.1
```
*Expected Output*:
- Streamlit web portal accessible at `http://localhost:8501`.
- Navigation active across Chat Assistant, Savings Dashboard, Compliance Audit Log, and CloudFormation Studio.

---

## Phase 2 (Enterprise Banking Production) Deployment Guide

### 1. Enterprise Infrastructure Containerization (`Dockerfile`)
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Prevent Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Banking Security, IAM & Governance Controls
1. **Zero AWS Credentials in Code**:
   - In production, use AWS IAM Execution Roles (ECR/AppRunner/ECS Task Roles) rather than hardcoded access keys.
2. **KMS Encryption Mandate Enforcement**:
   - All S3 storage buckets hosting CUR Parquet files and Glue metadata must use AWS Managed KMS keys (`aws/s3` or Customer Managed CMKs).
3. **AWS Service Catalog Integration**:
   - Remediation templates generated by `iac_generator.py` are pushed directly to an AWS Service Catalog Portfolio (`CloudIntel-Remediations-Portfolio`) via automated CloudFormation pipeline deployment.

---

## Health Check, Verification & Rollback Procedures

### 1. Verification Commands & Diagnostics

| Verification Step | Execution Command | Success Criteria |
| :--- | :--- | :--- |
| **Ingestion Check** | `python -c "import duckdb; con=duckdb.connect('data/processed/cloudintel.duckdb'); print(con.execute('SHOW TABLES').fetchall())"` | Returns all 5 core CloudIntel tables |
| **LLM Connection** | `python query_agent.py --test-connection` | Groq API connection successful (`200 OK`) |
| **Guardrails Test** | `python guardrails.py --run-tests` | Passes `RULE_S3_KMS`, `RULE_ECS_SIDECARS`, `RULE_LAMBDA_BOUNDS`, `RULE_NO_PUBLIC_ACCESS` |
| **Streamlit Health** | `curl -f http://localhost:8501/_stcore/health` | Returns HTTP `200 OK` |

### 2. Rollback & Emergency Procedures
1. **Local DuckDB Corruption**:
   - Delete `data/processed/cloudintel.duckdb` and rerun `python ingest.py` to regenerate cleanly from `data/raw/`.
2. **LLM Provider Outage / API Fallback**:
   - Switch `.env` variable `LLM_MODEL_NAME` or switch fallback provider endpoint in `llm_client.py`.
3. **Container Rollback (Phase 2)**:
   - Roll back AWS App Runner service / ECS Task Definition to previous immutable ECR image tag via AWS Management Console or AWS CLI:
     ```bash
     aws apprunner update-service --service-arn <SERVICE_ARN> --source-configuration ImageRepository={ImageIdentifier=<PREVIOUS_ECR_TAG>}
     ```

---

## Post-Deployment Operations & Maintenance Schedule

- **Daily**: Automated ETL execution (`ingest.py`) to process incremental Cloud Cost & Usage Reports (CUR).
- **Weekly**: Run `analyzer.py` cross-BU pattern check to surface shared optimization opportunities.
- **Monthly**: Audit `candidate_recommendations` table for compliance rejection logs and refine guardrail policy rules as bank compliance standards evolve.
