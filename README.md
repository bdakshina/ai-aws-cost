# CloudIntel — Enterprise AI FinOps Platform & Claude Code Plugin Architecture

CloudIntel is an enterprise-grade AI FinOps intelligence platform engineered to eliminate cloud waste across decentralized Business Units (BUs) in strict compliance with banking and financial sector standards.

Powered natively by the **Anthropic Claude API (Claude 3.5 Sonnet / Claude 3.7 Sonnet)** and architected as an integrated **Claude Code Plugin & Anthropic Agent SDK ecosystem (`claude-code-plugins`)**, CloudIntel brings proactive FinOps intelligence directly into developer IDEs, terminals, and automated CI/CD pipelines.

---

## Key Features

- **Native Anthropic Claude API Cognitive Engine**:
  - **Claude 3.7 Sonnet** (`claude-3-7-sonnet-20250219`) — Extended thinking for complex cross-BU cost allocation math and multi-variable FinOps reasoning.
  - **Claude 3.5 Sonnet** (`claude-3-5-sonnet-20241022`) — High-precision native tool calling and compliant AWS CloudFormation template authoring.
  - **Claude 3.5 Haiku** (`claude-3-5-haiku-20241022`) — High-speed billing record classification and anomaly triage.
  - **Prompt Caching (`cache_control`)** — Caches static AWS schemas, pricing tables, and banking compliance rules for **up to 90% API cost reduction** and **80% lower latency**.
- **Claude Code CLI & IDE Integration**:
  - Native slash commands in developer workflows: `/finops-query`, `/finops-analyze`, `/finops-remediate`, `/finops-guardrails`, `/finops-ingest`.
- **Anthropic Agent SDK Framework (`agent-sdk-example/`)**:
  - Autonomous multi-turn FinOps agent (`finops_autonomous_agent.py`) with tool-calling loops and golden benchmark evaluation suites (`agent-sdk-example/evaluation/`).
- **In-Process Analytical Database (DuckDB)**:
  - Columnar OLAP engine (`data/processed/cloudintel.duckdb`) executing fast SQL aggregations over raw billing records and CloudWatch metrics without external database costs.
- **Multi-Resource FinOps Scope**:
  - **Amazon ECS (EC2 launch type)**: Container vCPU/RAM reservation vs. P95 actual utilization.
  - **AWS Lambda**: Memory allocation sizing, duration metrics, and idle provisioned concurrency.
  - **Amazon S3**: Inactive Standard storage tiering (Glacier Instant/Deep Archive) and object lifecycle management.
  - **Amazon RDS & Databases**: Idle instances, underutilized IOPS, and unattached storage volumes.
- **Banking Security & Compliance Guardrails Engine**:
  - **Mandatory KMS Encryption (`RULE_S3_KMS`)**: Programmatically intercepts and rejects any AI recommendation attempting to delete or downgrade `aws_kms_key` / `SSE-KMS`.
  - **Preserve Container Sidecars (`RULE_ECS_SIDECARS`)**: Mandates retention of security monitoring, audit logging, and telemetry containers in `AWS::ECS::TaskDefinition`.
  - **Lambda Telemetry Buffer (`RULE_LAMBDA_BOUNDS`)**: Guarantees memory buffer headroom for enterprise tracing (AWS X-Ray).
  - **Zero Public Access (`RULE_NO_PUBLIC_ACCESS`)**: Enforces `PublicAccessBlockConfiguration` on all generated S3 remediation templates.
- **AWS Service Catalog & CloudFormation Studio**:
  - Auto-synthesizes validated AWS CloudFormation YAML/JSON templates formatted for enterprise **AWS Service Catalog** portfolio publishing.
- **VS Code DevContainer & GitLab CI/CD**:
  - Pre-configured `.devcontainer/` environment and `.gitlab/` CI/CD automated linting, pytest, and security compliance audits.

---

## Target Repository Hierarchy

```plaintext
claude-code-plugins/
├── .claude-plugin/                        # Plugin manifest & marketplace configuration
│   ├── manifest.json                      # Plugin metadata, tool definitions, skills, hooks
│   └── plugin-config.yaml                 # FinOps plugin lifecycle & runtime config
│
├── .claude/                               # Claude Code workspace settings & prompt definitions
│   ├── settings.json                      # Workspace permissions, tool access rules, model presets
│   ├── commands/                          # Custom slash commands for Claude Code CLI
│   │   ├── finops-query.md                # /finops-query — Natural language Text-to-SQL FinOps Q&A
│   │   ├── finops-analyze.md              # /finops-analyze — Multi-dimensional waste detection
│   │   ├── finops-remediate.md            # /finops-remediate — CloudFormation template generation
│   │   ├── finops-guardrails.md           # /finops-guardrails — Compliance audit & policy logs
│   │   └── finops-ingest.md               # /finops-ingest — Live AWS / mock CUR data ingestion
│   └── rules/                             # Behavioral rules and banking compliance constraints
│       └── finops-compliance-rules.md     # Mandatory KMS, sidecar retention, zero public access
│
├── .devcontainer/                         # Containerized development environment
│   ├── devcontainer.json                  # VS Code / Codespaces dev container specification
│   ├── Dockerfile                         # Python 3.11+, AWS CLI v2, DuckDB, Claude Code CLI tools
│   └── scripts/
│       └── setup-permissions.sh           # Custom credential handlers & sandbox security policies
│
├── .gitlab/                               # GitLab CI/CD pipelines & automated integrations
│   ├── ci/
│   │   ├── lint-and-test.gitlab-ci.yml    # Pytest, Black, Flake8, MyPy type checks
│   │   ├── guardrail-audit.gitlab-ci.yml  # Automated banking security compliance test suite
│   │   └── iac-validate.gitlab-ci.yml     # cfn-lint and cfn-nag CloudFormation security validation
│   └── integrations/
│       └── drawio-export.sh               # Drawio plugin integrations for auto-generating architecture SVGs
│
├── agent-sdk-example/                     # Anthropic Agent SDK reference implementations & evaluations
│   ├── finops_autonomous_agent.py        # Multi-turn autonomous FinOps agent using Anthropic Claude API
│   ├── custom_tools.py                    # Anthropic Agent SDK tool wrappers (DuckDB, Boto3, Guardrails)
│   ├── evaluation/                        # Evaluation benchmarks & scoring framework
│   │   ├── eval_benchmarks.json           # 50+ golden benchmark queries & expected SQL/cost insights
│   │   ├── evaluate_accuracy.py           # Text-to-SQL precision & hallucination evaluation runner
│   │   └── benchmark_results.md           # Accuracy, latency, and guardrail compliance reports
│   └── README.md                          # Guide for running & extending the Agent SDK examples
│
├── docs/                                  # Project & plugin documentation
│   ├── PROBLEM_STATEMENT.md               # Vision, problem definition, and acceptance criteria
│   ├── ARCHITECTURE.md                    # Detailed system architecture specification
│   ├── DEVELOPER_GUIDE.md                 # Contributor setup & developer guide
│   ├── PLUGIN_INSTALLATION_GUIDE.md       # Plugin installation & Claude Code configuration guide
│   ├── BANKING_GUARDRAILS_SPEC.md         # Detailed banking security rules & policy specifications
│   ├── SERVICE_CATALOG_INTEGRATION.md     # AWS Service Catalog portfolio & CloudFormation integration
│   ├── USER_GUIDE.md                      # End-user operational guide (CLI & UI workflows)
│   ├── deployment-plan.md                 # Deployment & environment promotion plan
│   └── Implementation-plan.md             # Phased engineering implementation plan
│
├── plugins/                               # Core plugin modules
│   └── finops-cost-optimizer/             # FinOps Cost Optimizer Claude Code Plugin
│       ├── __init__.py
│       ├── manifest.json                  # Plugin-specific capability declarations
│       ├── tools/                         # Modular tool implementations (invoked by Claude / Agent SDK)
│       │   ├── __init__.py
│       │   ├── data_ingest_tool.py        # Ingests CUR, ECS, Lambda, S3, RDS metrics into DuckDB
│       │   ├── query_engine_tool.py       # Text-to-SQL translation & DuckDB query execution via Claude API
│       │   ├── waste_analyzer_tool.py     # Multi-resource pattern recognition & waste scoring
│       │   ├── guardrails_tool.py         # Banking compliance filter (KMS, sidecars, security)
│       │   ├── iac_generator_tool.py      # Compliant AWS CloudFormation & Service Catalog generator
│       │   └── aws_connector_tool.py      # Boto3 live AWS Cost Explorer & CloudWatch connector
│       ├── core/                          # Underlying business logic engines
│       │   ├── __init__.py
│       │   ├── claude_client.py           # Native Anthropic Claude API wrapper with caching & retry logic
│       │   ├── ingest_engine.py           # ETL normalization & DuckDB schema management
│       │   ├── analyzer_engine.py         # 7 major waste category analytical algorithms
│       │   ├── guardrails_engine.py       # Policy-driven compliance validation logic
│       │   └── iac_engine.py              # CloudFormation YAML/JSON AST & template builder
│       ├── skills/                        # Claude Code skill instructions
│       │   └── finops-analysis/
│       │       └── SKILL.md               # Cheatsheet & prompt instructions for FinOps workflows
│       └── accounts.json                  # Enterprise AWS account registry & BU mappings
│
├── tests/                                 # Automated test suites
│   ├── __init__.py
│   ├── conftest.py                        # Pytest fixtures, mock DuckDB, and mock Claude API responses
│   ├── unit/                              # Unit tests for core engines
│   │   ├── test_claude_client.py          # Tests Anthropic API connectivity, caching, and message handling
│   │   ├── test_ingest.py                 # Tests CSV/JSON ingestion, schema normalization
│   │   ├── test_query_agent.py            # Tests Text-to-SQL generation and context explainer
│   │   ├── test_analyzer.py               # Tests ECS, Lambda, S3, RDS waste detection logic
│   │   ├── test_guardrails.py             # Tests KMS mandate, sidecar protection, public access blocks
│   │   └── test_iac_generator.py          # Tests CloudFormation synthesis & syntax validity
│   ├── integration/                       # Integration & tool-calling tests
│   │   ├── test_claude_tools.py           # Tests Claude Code plugin tool bindings
│   │   ├── test_agent_sdk_workflow.py     # Tests end-to-end multi-turn Agent SDK execution
│   │   └── test_aws_connector.py          # Tests live/mock Boto3 multi-account polling
│   └── security/                          # Security & compliance regression tests
│       └── test_banking_compliance.py     # Rejection tests for unsafe AI cost-saving proposals
│
├── .env.example                           # Template for environment variables (ANTHROPIC_API_KEY, AWS configs)
├── .gitignore                             # Git ignore rules (data files, duckdb, caches, secrets)
├── requirements.txt                       # Python dependencies (anthropic, duckdb, boto3, pydantic, etc.)
└── README.md                              # This document
```

---

## Environment Configuration (`.env`)

Create a `.env` file in the project root directory:

```env
# 1. Anthropic Claude API Configuration
ANTHROPIC_API_KEY=sk-ant-api03-your_anthropic_api_key_here
CLAUDE_PRIMARY_MODEL=claude-3-7-sonnet-20250219
CLAUDE_FAST_MODEL=claude-3-5-haiku-20241022

# 2. AWS Credentials (for live multi-account polling)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
AWS_SESSION_TOKEN=your_optional_session_token_here
AWS_DEFAULT_REGION=us-east-1

# 3. Application & Compliance Settings
GUARDRAILS_MODE=ENFORCE
ENFORCE_KMS_MANDATE=true
ENFORCE_ECS_SIDECARS=true
ENFORCE_LAMBDA_MEMORY_BOUNDS=true
ENFORCE_ZERO_PUBLIC_ACCESS=true
ACCOUNTS_CONFIG_PATH=accounts.json
DUCKDB_PATH=data/processed/cloudintel.duckdb
DATA_RAW_DIR=data/raw
```

---

## Quickstart Guide

### Option A: VS Code DevContainer (Recommended)
1. Open the project in **Visual Studio Code**.
2. Select **"Reopen in Container"** when prompted.
3. The environment automatically sets up Python 3.11+, AWS CLI, DuckDB, Claude Code CLI, and project dependencies.

### Option B: Local Virtual Environment
```bash
# 1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
# source venv/bin/activate    # Linux / macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure .env file
cp .env.example .env
```

### Run Data Ingestion (ETL)
```bash
# Ingest raw CUR and telemetry datasets into DuckDB
python plugins/finops-cost-optimizer/tools/data_ingest_tool.py

# Live AWS Non-Prod Polling Mode
python plugins/finops-cost-optimizer/tools/data_ingest_tool.py --use-aws
```

### Run Claude Code CLI Slash Commands
```bash
# Natural Language Text-to-SQL Query
claude /finops-query "Which Business Unit spent the most on Lambda last week and why?"

# Proactive Multi-Resource Waste Analysis
claude /finops-analyze

# Synthesize Compliant CloudFormation Remediation
claude /finops-remediate --recommendation-id REC-S3-001
```

---

## Testing & Quality Gates

```bash
# 1. Run all unit tests
pytest tests/unit/ -v

# 2. Run banking compliance security guardrail tests
pytest tests/security/test_banking_compliance.py -v

# 3. Run Anthropic Agent SDK evaluation benchmarks
python agent-sdk-example/evaluation/evaluate_accuracy.py
```

---

## Documentation Index

- **[PROBLEM_STATEMENT.md](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/PROBLEM_STATEMENT.md)** — Project vision, Claude Code Plugin proposal, and acceptance criteria.
- **[ARCHITECTURE.md](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/ARCHITECTURE.md)** — Comprehensive system architecture, sequence flows, and DuckDB schemas.
- **[Implementation-plan.md](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/Implementation-plan.md)** — 5-phase engineering implementation roadmap.
- **[deployment-plan.md](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/deployment-plan.md)** — Multi-phase operational promotion & DevContainer guide.
- **[edge-case.md](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/edge-case.md)** — Corner scenarios, API rate limiting, and failure mitigations.
- **[DEVELOPER_GUIDE.md](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/DEVELOPER_GUIDE.md)** — Contributor onboarding & local development workflows.

---

*CloudIntel: Powered natively by Anthropic Claude API for Autonomous Enterprise FinOps.*
