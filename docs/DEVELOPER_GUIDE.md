# CloudIntel — Developer & Contributor Guide (Claude Code Plugin Architecture)

---

## 1. Executive Summary & Architecture Overview

Welcome to the **CloudIntel Developer Guide**. This document provides detailed technical specifications, setup instructions, extension patterns, and testing guidelines for software engineers, DevOps/FinOps developers, and AI engineers working on the **CloudIntel Claude Code Plugin & Anthropic Agent SDK ecosystem (`claude-code-plugins`)**.

### Repository Structure
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
│   ├── DEVELOPER_GUIDE.md                 # This document
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
└── README.md                              # Root project overview, quickstart, and plugin showcase
```

---

## 2. Developer Environment Setup

### Option A: VS Code DevContainer (Recommended)
1. Open the workspace root in Visual Studio Code.
2. Select **"Reopen in Container"** when prompted.
3. All dependencies, CLI tools (Claude Code CLI, AWS CLI, DuckDB), and pre-configured environment variables will be provisioned automatically.

### Option B: Local Python Virtual Environment
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

Edit `.env` to include your Anthropic API Key:
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
CLAUDE_PRIMARY_MODEL=claude-3-7-sonnet-20250219
CLAUDE_FAST_MODEL=claude-3-5-haiku-20241022
DUCKDB_PATH=data/processed/cloudintel.duckdb
GUARDRAILS_MODE=ENFORCE
```

---

## 3. Core Development Workflows

### 3.1 Adding a New Cloud Resource Category
1. **DuckDB Schema**: Add the new resource table creation in `plugins/finops-cost-optimizer/core/ingest_engine.py`.
2. **Data Ingestion**: Add parsing in `plugins/finops-cost-optimizer/tools/data_ingest_tool.py` and Boto3 polling in `aws_connector_tool.py`.
3. **Waste Scanner Algorithm**: Add pattern recognition logic in `plugins/finops-cost-optimizer/core/analyzer_engine.py`.
4. **Banking Guardrails**: Add corresponding compliance rules in `plugins/finops-cost-optimizer/core/guardrails_engine.py`.
5. **IaC Synthesizer**: Add CloudFormation generation rules in `plugins/finops-cost-optimizer/core/iac_engine.py`.

### 3.2 Running Automated Test Suites
```bash
# Run all unit tests
pytest tests/unit/ -v

# Run banking compliance security tests
pytest tests/security/test_banking_compliance.py -v

# Run Anthropic Agent SDK evaluation benchmarks
python agent-sdk-example/evaluation/evaluate_accuracy.py
```

---

*CloudIntel Developer Guide — Standardized on Claude Code Plugin & Anthropic Agent SDK.*
