# Implementation Plan — CloudIntel: Enterprise AI FinOps Platform & Claude Code Plugin Architecture

---

## 1. Executive Summary & Vision

**CloudIntel** is an enterprise AI FinOps platform designed to ingest cloud cost and usage data, analyze multi-dimensional waste patterns across decentralized Business Units (BUs), enforce strict banking security and compliance guardrails, and automatically generate compliant AWS CloudFormation templates ready for **AWS Service Catalog** integration.

This document details the complete end-to-end technical implementation plan for transforming CloudIntel into a native **Claude Code Plugin** and **Anthropic Agent SDK ecosystem (`claude-code-plugins`)**, powered by the **Anthropic Claude API (Claude 3.5 Sonnet / Claude 3.7 Sonnet)**.

---

## 2. Technical Strategy & Multi-Phase Roadmap

| Category | Phase 1: Local / Sandbox Scope | Phase 2: Enterprise Production Scale |
| :--- | :--- | :--- |
| **Resource Focus** | **Amazon ECS (EC2)**, **AWS Lambda**, **Amazon S3**, **Amazon RDS** | All Enterprise AWS Resources (EC2, S3, RDS, Lambda, DynamoDB, VPC/NAT) |
| **AI / Cognitive Engine** | **Anthropic Claude API (`claude-3-7-sonnet-20250219` / `claude-3-5-sonnet-20241022`)** | Enterprise Anthropic Claude API with Prompt Caching & Dedicated Endpoints |
| **Fast Triage Engine** | **Anthropic Claude 3.5 Haiku (`claude-3-5-haiku-20241022`)** | High-throughput billing data normalization & alert routing |
| **Agent Framework** | **Anthropic Agent SDK (`anthropic`)** | Autonomous multi-turn FinOps agent orchestration with tool use |
| **Developer Interface** | **Claude Code CLI & IDE Plugins** (`/finops-query`, `/finops-analyze`, `/finops-remediate`) | Centralized Developer FinOps Portal & CI/CD Pipelines |
| **AWS Authentication** | **AWS Access Keys / SSO** (`.env` or local profile) | **System Account Access** (Central System IAM Execution Role federating AWS Organizations) |
| **Account Discovery** | **`accounts.json` Configuration** | **AWS Organizations Auto-Discovery API** |
| **Compliance Layer** | **Banking Guardrails Engine** (`guardrails_tool.py`) | Enterprise Policy Engine (AWS OPA / Sentinel / AWS Config integration) |
| **Database Engine** | **DuckDB** (`data/processed/cloudintel.duckdb`) | **AWS Athena / Amazon Redshift Serverless** |
| **Storage / Data Lake** | Local Directory (`data/raw/`, `data/processed/`) | AWS S3 Data Lake + AWS Glue Data Catalog |
| **IaC Output** | **AWS CloudFormation (YAML/JSON)** & Service Catalog Product Manifests | Automated AWS Service Catalog Portfolio Pipelines (CodePipeline) |

---

## 3. Target Repository Hierarchy

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
│   ├── DEVELOPER_GUIDE.md                 # Setup, local development, and plugin authoring guide
│   ├── PLUGIN_INSTALLATION_GUIDE.md       # Plugin installation & Claude Code configuration guide
│   ├── BANKING_GUARDRAILS_SPEC.md         # Detailed banking security rules & policy specifications
│   ├── SERVICE_CATALOG_INTEGRATION.md     # AWS Service Catalog portfolio & CloudFormation integration
│   ├── USER_GUIDE.md                      # End-user operational guide (CLI & UI workflows)
│   ├── deployment-plan.md                 # Deployment & environment promotion plan
│   └── Implementation-plan.md             # This document
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

## 4. Detailed Component Implementation Specifications

### 4.1 Native Claude API Client (`core/claude_client.py`)
- Uses the official `anthropic` Python package.
- Implements **Prompt Caching** (`cache_control: {"type": "ephemeral"}`) on system prompts, DuckDB schemas, and banking guardrail definitions to save 90% cost.
- Implements tool-calling schemas matching Anthropic function-calling specifications.
- Supports Claude 3.7 Sonnet Extended Thinking mode for complex multi-turn optimization calculations.

### 4.2 Modular Plugin Tools (`plugins/finops-cost-optimizer/tools/`)
1. **`data_ingest_tool.py`**: Ingests raw CUR and CloudWatch metrics into DuckDB.
2. **`query_engine_tool.py`**: Translates natural language questions to DuckDB SQL queries and returns contextual explanations.
3. **`waste_analyzer_tool.py`**: Evaluates over-provisioned ECS containers, idle Lambda functions, un-lifecycle S3 objects, and underutilized RDS instances.
4. **`guardrails_tool.py`**: Enforces `RULE_S3_KMS`, `RULE_ECS_SIDECARS`, `RULE_LAMBDA_BOUNDS`, and `RULE_NO_PUBLIC_ACCESS`.
5. **`iac_generator_tool.py`**: Uses Claude 3.5/3.7 Sonnet to author valid, formatted CloudFormation templates.
6. **`aws_connector_tool.py`**: Interfaces with live AWS APIs (Cost Explorer, CloudWatch, ECS, Lambda, S3) using Boto3.

### 4.3 Anthropic Agent SDK Implementation (`agent-sdk-example/`)
- Implements `finops_autonomous_agent.py` using Anthropic Agent SDK workflows.
- Contains custom tool wrappers (`custom_tools.py`) exposing DuckDB, Boto3, and Guardrails to Claude.
- Contains benchmark evaluation suite (`evaluation/eval_benchmarks.json` and `evaluation/evaluate_accuracy.py`) measuring precision, latency, and guardrail enforcement.

---

## 5. Step-by-Step Engineering Execution Plan

### Phase 1: Foundation & Hierarchy Scaffolding
- [ ] Create folder structure: `.claude-plugin/`, `.claude/`, `.devcontainer/`, `.gitlab/`, `agent-sdk-example/`, `docs/`, `plugins/`, `tests/`.
- [ ] Author `.devcontainer/devcontainer.json`, `Dockerfile`, and `setup-permissions.sh`.
- [ ] Author `.claude/settings.json`, custom commands (`/finops-query`, `/finops-analyze`, `/finops-remediate`, `/finops-guardrails`, `/finops-ingest`), and rules (`finops-compliance-rules.md`).
- [ ] Author `.claude-plugin/manifest.json` and `plugin-config.yaml`.
- [ ] Update `requirements.txt` with `anthropic>=0.40.0`, `duckdb>=1.0.0`, `boto3>=1.34.0`, `pydantic>=2.0.0`, `pyyaml`, `pytest`.

### Phase 2: Core Plugin Modularization (`plugins/finops-cost-optimizer`)
- [ ] Implement `core/claude_client.py` with Messages API, Prompt Caching, and retry logic.
- [ ] Implement `core/ingest_engine.py` and `tools/data_ingest_tool.py` for multi-service DuckDB ingestion.
- [ ] Implement `tools/query_engine_tool.py` for Text-to-SQL translation and synthesis.
- [ ] Implement `core/analyzer_engine.py` and `tools/waste_analyzer_tool.py` for multi-dimensional waste detection.
- [ ] Implement `core/guardrails_engine.py` and `tools/guardrails_tool.py` with banking policy interceptors.
- [ ] Implement `core/iac_engine.py` and `tools/iac_generator_tool.py` for CloudFormation template generation.
- [ ] Implement `tools/aws_connector_tool.py` for live AWS multi-account Boto3 polling.
- [ ] Author `skills/finops-analysis/SKILL.md` cheatsheet.

### Phase 3: Anthropic Agent SDK Implementation (`agent-sdk-example/`)
- [ ] Implement `agent-sdk-example/custom_tools.py` with typed tool definitions.
- [ ] Implement `agent-sdk-example/finops_autonomous_agent.py` multi-turn reasoning agent.
- [ ] Create `agent-sdk-example/evaluation/eval_benchmarks.json` with 50+ golden benchmark scenarios.
- [ ] Implement `agent-sdk-example/evaluation/evaluate_accuracy.py` runner to score accuracy and guardrail safety.

### Phase 4: CI/CD & Automated Test Suites (`.gitlab/` & `tests/`)
- [ ] Create unit test suites in `tests/unit/` (`test_claude_client.py`, `test_ingest.py`, `test_query_agent.py`, `test_analyzer.py`, `test_guardrails.py`, `test_iac_generator.py`).
- [ ] Create integration test suites in `tests/integration/` (`test_claude_tools.py`, `test_agent_sdk_workflow.py`, `test_aws_connector.py`).
- [ ] Create security test suite in `tests/security/test_banking_compliance.py` for adversarial injection tests.
- [ ] Configure GitLab CI/CD pipelines in `.gitlab/ci/` (`lint-and-test`, `guardrail-audit`, `iac-validate`).

### Phase 5: Documentation & Validation (`docs/`)
- [ ] Verify complete alignment across `docs/PROBLEM_STATEMENT.md`, `docs/ARCHITECTURE.md`, `docs/deployment-plan.md`, `docs/Implementation-plan.md`, `docs/DEVELOPER_GUIDE.md`, and `docs/PLUGIN_INSTALLATION_GUIDE.md`.
- [ ] Perform end-to-end dry-run of Claude Code CLI slash commands and Agent SDK workflows.

---

## 6. Verification & Quality Gates

| Verification Target | Command / Test | Acceptance Criteria |
| :--- | :--- | :--- |
| **Unit Tests** | `pytest tests/unit/` | 100% pass rate across all engine modules |
| **Security Guardrails** | `pytest tests/security/test_banking_compliance.py` | 100% interception of unsafe AI cost-saving proposals |
| **Agent SDK Evaluation** | `python agent-sdk-example/evaluation/evaluate_accuracy.py` | >95% Text-to-SQL precision and zero guardrail violations |
| **CloudFormation Syntax** | `cfn-lint aws_nonprod_deploy.yaml` | Zero errors or blocking warnings |
| **DevContainer Build** | VS Code Dev Container initialization | Clean build with all tools and permissions active |

---

*CloudIntel Implementation Plan — Engineering Roadmap for Claude Code Plugin & Anthropic Agent SDK.*
