# CloudIntel — Enterprise AI FinOps Platform & Claude Code Plugin Ecosystem
## System Architecture Specification

---

## 1. Executive Summary & Vision

**CloudIntel** is an enterprise-grade AI FinOps intelligence platform engineered to eliminate cloud waste across decentralized Business Units (BUs) in strict compliance with banking and financial sector standards.

Traditional cloud management tools produce complex JSON logs, obscure cost graphs, and disconnected dashboards that fail to provide actionable clarity to engineering and business stakeholders. Furthermore, in banking environments, cost optimization is severely constrained: AI recommendations must **never** weaken security (e.g., removing AWS KMS encryption, dropping container monitoring sidecars, or opening public access), and all infrastructure provisioning is strictly governed by **AWS Service Catalog** using compliant **AWS CloudFormation** templates.

To bring proactive FinOps intelligence directly into developer workflows, **CloudIntel is powered natively by the Anthropic Claude API (Claude 3.5 Sonnet / Claude 3.7 Sonnet) and architected as an integrated Claude Code Plugin and Anthropic Agent SDK ecosystem (`claude-code-plugins`)**.

Stakeholders interact with their cloud infrastructure through natural language inside **Claude Code CLI**, IDEs, and automated CI/CD pipelines. The AI agent autonomously ingests multi-account telemetry and billing data into an in-process DuckDB OLAP engine, executes multi-dimensional waste reasoning, enforces rigorous **Banking Security & Compliance Guardrails**, and auto-generates compliant **AWS CloudFormation** templates formatted for enterprise **AWS Service Catalog** deployment.

---

## 2. Technology & Architectural Strategy Matrix

| Component | Specification / Technology | Purpose in Platform |
| :--- | :--- | :--- |
| **Primary AI Engine** | **Anthropic Claude API (`claude-3-7-sonnet-20250219` / `claude-3-5-sonnet-20241022`)** | Deep FinOps reasoning, accurate Text-to-SQL generation, native tool calling, and high-fidelity CloudFormation template authoring. |
| **High-Throughput Triage** | **Anthropic Claude 3.5 Haiku (`claude-3-5-haiku-20241022`)** | Rapid billing record classification, log normalization, and real-time cost anomaly triage. |
| **Agent Orchestration** | **Anthropic Agent SDK (`anthropic`)** | Multi-turn autonomous reasoning, tool calling, scratchpad memory, and structured Pydantic outputs. |
| **Developer Interface** | **Claude Code Plugin & Slash Commands** | Direct integration into Claude Code CLI & IDE (`/finops-query`, `/finops-analyze`, `/finops-remediate`). |
| **Prompt Optimization** | **Anthropic Prompt Caching (`cache_control`)** | Caching database schemas, banking compliance rules, and AWS pricing models for 90% API cost reduction. |
| **Analytical Database** | **DuckDB (In-Process Columnar OLAP)** | High-performance analytical SQL queries over raw billing exports and CloudWatch metric logs without external database infrastructure costs. |
| **Cloud Target** | **Amazon Web Services (AWS)** | Ingestion and remediation across ECS (EC2 launch type), Lambda, S3, RDS, DynamoDB, and VPC Networking. |
| **AWS Authentication** | **AWS IAM Role Federation / Boto3** | System account federation across multi-account enterprise registries (`accounts.json` / AWS Organizations). |
| **Compliance Layer** | **Banking Guardrails Engine** | Programmatic verification blocking unsafe AI recommendations (Mandatory KMS, sidecar retention, zero public access). |
| **IaC Remediation** | **AWS CloudFormation & AWS Service Catalog** | Generates standardized, enterprise-compliant YAML/JSON CloudFormation templates ready for Service Catalog portfolios. |
| **Containerization** | **VS Code Dev Containers (`.devcontainer`)** | Reproducible development environment with pre-installed Claude CLI, AWS CLI, DuckDB, and security sandboxes. |
| **CI/CD Automation** | **GitLab CI/CD (`.gitlab/`)** | Automated linting, pytest suites, banking compliance verification, and CloudFormation security audits. |

---

## 3. High-Level Architecture Diagram

```mermaid
flowchart TB
    subgraph User_Interface_Layer ["1. Developer & Platform Interface Layer"]
        CLI["Claude Code CLI\n(/finops-query, /finops-analyze, /finops-remediate)"]
        IDE["IDE Plugin Integration\n(VS Code / JetBrains via Claude Code)"]
        WebUI["Streamlit FinOps Portal\n(Visual Dashboard & CloudFormation Studio)"]
    end

    subgraph Agent_Layer ["2. Claude Code Plugin & Anthropic Agent SDK Layer"]
        AgentSDK["Anthropic Agent SDK Orchestrator\n(finops_autonomous_agent.py)"]
        
        subgraph Plugin_Tools ["finops-cost-optimizer Plugin Tools"]
            T1["data_ingest_tool\n(Ingest CUR & Metrics)"]
            T2["query_engine_tool\n(Text-to-SQL & Explainer)"]
            T3["waste_analyzer_tool\n(Multi-Resource Reasoning)"]
            T4["guardrails_tool\n(Banking Security Validator)"]
            T5["iac_generator_tool\n(AWS CloudFormation Generator)"]
            T6["aws_connector_tool\n(Boto3 Live Polling)"]
        end
    end

    subgraph Claude_API_Layer ["3. Anthropic Claude API Cognitive Layer"]
        ClaudeClient["claude_client.py\n(Messages API + Prompt Caching)"]
        Claude37["Claude 3.7 Sonnet\n(Extended Thinking & FinOps Math)"]
        Claude35["Claude 3.5 Sonnet\n(Tool Calling & IaC Synthesis)"]
        ClaudeHaiku["Claude 3.5 Haiku\n(Fast Triage & Tagging)"]
        
        ClaudeClient --> Claude37
        ClaudeClient --> Claude35
        ClaudeClient --> ClaudeHaiku
    end

    subgraph Data_Layer ["4. Analytical Data & Cloud Infrastructure Layer"]
        DuckDB[("DuckDB OLAP Engine\n(cloudintel.duckdb)")]
        LiveAWS["Live AWS Infrastructure\n(Cost Explorer, ECS, Lambda, S3, RDS)"]
        RawFiles["Raw Billing Exports & JSON Logs\n(data/raw/)"]
        GuardrailsEngine["Banking Guardrails Engine\n(KMS Mandate, Sidecars, Public Access)"]
        CFNOutput["Compliant CloudFormation Templates\n(AWS Service Catalog Portfolios)"]
    end

    %% Connections
    CLI <--> AgentSDK
    IDE <--> AgentSDK
    WebUI <--> AgentSDK
    
    AgentSDK <--> ClaudeClient
    AgentSDK --> T1
    AgentSDK --> T2
    AgentSDK --> T3
    AgentSDK --> T4
    AgentSDK --> T5
    AgentSDK --> T6
    
    T1 <--> RawFiles
    T1 <--> DuckDB
    T6 <--> LiveAWS
    T6 --> T1
    T2 <--> DuckDB
    T3 <--> DuckDB
    T3 --> T4
    T4 <--> GuardrailsEngine
    T4 --> T5
    T5 --> CFNOutput
```

---

## 4. End-to-End System Sequence & Data Flow

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer / FinOps Lead
    participant CC as Claude Code CLI (.claude/)
    participant SDK as Anthropic Agent SDK (finops_autonomous_agent.py)
    participant Claude as Anthropic Claude API (Claude 3.5/3.7 Sonnet)
    participant Tools as Plugin Tools (plugins/finops-cost-optimizer/)
    participant DB as DuckDB (cloudintel.duckdb)
    participant GE as Banking Guardrails Engine (guardrails_engine.py)
    participant IaC as CloudFormation Engine (iac_engine.py)
    participant SC as AWS Service Catalog

    rect rgb(240, 248, 255)
        note over Dev, DB: Phase 1: Data Ingestion & DuckDB Population
        Dev->>CC: Run `/finops-ingest` (or schedule automatic polling)
        CC->>SDK: Trigger Data Ingestion Workflow
        SDK->>Tools: Call `data_ingest_tool` (with live Boto3 or mock CUR)
        Tools->>DB: Populate normalized tables (daily_cost, ecs_metrics, lambda_metrics, s3_metrics)
        DB-->>Tools: Tables populated & indexed
        Tools-->>SDK: Return ingestion summary
        SDK-->>CC: Display ingestion status & record counts
    end

    rect rgb(255, 245, 238)
        note over Dev, Claude: Phase 2: Natural Language Query & Text-to-SQL
        Dev->>CC: Run `/finops-query "Which BU spent the most on Lambda last week and why?"`
        CC->>SDK: Forward natural language query
        SDK->>Claude: Messages API with DuckDB Schema & System Prompt (Prompt Cached)
        Claude-->>SDK: Return Tool Call: `execute_duckdb_sql(query=...)`
        SDK->>Tools: Execute `query_engine_tool` with SQL
        Tools->>DB: Execute ANSI SQL Query
        DB-->>Tools: Return tabular result set
        Tools-->>SDK: Return query results
        SDK->>Claude: Pass SQL results back for synthesis
        Claude-->>SDK: Synthesize business context & cost driver explanation
        SDK-->>CC: Return formatted response in terminal / IDE
    end

    rect rgb(245, 255, 250)
        note over Dev, SC: Phase 3: Proactive Waste Detection & Banking Guardrails
        Dev->>CC: Run `/finops-analyze`
        CC->>SDK: Trigger Multi-Dimensional Waste Analysis
        SDK->>Tools: Call `waste_analyzer_tool`
        Tools->>DB: Query over-provisioned ECS tasks, idle Lambdas, un-lifecycle S3 objects
        DB-->>Tools: Return raw candidate inefficiencies
        Tools->>Claude: Extended Thinking Prompt: Evaluate cross-BU waste patterns & ROI
        Claude-->>Tools: Return candidate optimization recommendations
        
        loop For Each Candidate Recommendation
            Tools->>GE: Intercept & validate candidate via `guardrails_tool`
            GE-->>GE: Check S3 KMS Mandate, Container Sidecars, & Zero Public Access
            alt Non-Compliant (e.g. Attempted KMS key deletion)
                GE-->>Tools: REJECTED (Violation Code: REJECTED_KMS_MANDATE)
                Tools-->>SDK: Log rejected candidate to compliance audit table
            else Compliant (Preserves all banking security rules)
                GE-->>Tools: APPROVED
                Tools-->>SDK: Add to approved recommendations list
            end
        end
        
        SDK-->>CC: Render interactive recommendations table with savings estimates & compliance badges
    end

    rect rgb(255, 250, 240)
        note over Dev, SC: Phase 4: Automated CloudFormation Synthesis & Service Catalog Integration
        Dev->>CC: Run `/finops-remediate --recommendation-id REC-S3-001`
        CC->>SDK: Trigger Remediation Synthesis
        SDK->>Tools: Call `iac_generator_tool`
        Tools->>Claude: Generate compliant CloudFormation YAML preserving KMS & parameters
        Claude-->>Tools: Return synthesized CloudFormation template
        Tools->>IaC: Validate YAML syntax & Service Catalog parameter structure
        IaC-->>SDK: Return validated CloudFormation template & Service Catalog manifest
        SDK-->>CC: Display CloudFormation code with option to deploy to AWS Service Catalog
        Dev->>SC: Deploy to AWS Service Catalog Non-Prod Portfolio
    end
```

---

## 5. Repository Architecture & Component Breakdown

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
│   ├── ARCHITECTURE.md                    # This document (System architecture specification)
│   ├── DEVELOPER_GUIDE.md                 # Local setup and plugin development guide
│   ├── PLUGIN_INSTALLATION_GUIDE.md       # Plugin installation & Claude Code configuration guide
│   ├── BANKING_GUARDRAILS_SPEC.md         # Detailed banking security policies & rule IDs
│   ├── SERVICE_CATALOG_INTEGRATION.md     # AWS Service Catalog portfolio deployment manual
│   ├── USER_GUIDE.md                      # End-user operational guide
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

## 6. Detailed Module Specifications

### 6.1 `claude_client.py` (Anthropic Claude API Wrapper)
- **Purpose**: Provides a resilient, type-safe interface to the Anthropic Messages API (`anthropic` SDK) with built-in **Prompt Caching** and exponential backoff retry handling.
- **Key Features**:
  - Automatically wraps system prompts, database schemas, and banking guardrail rules in `cache_control: {"type": "ephemeral"}` blocks.
  - Dynamically routes complex multi-BU reasoning and mathematical calculations to `claude-3-7-sonnet-20250219` with Extended Thinking enabled, and high-throughput tagging to `claude-3-5-haiku-20241022`.
  - Handles JSON Schema validation for all Claude tool calls.

### 6.2 `plugins/finops-cost-optimizer/tools/`
1. **`data_ingest_tool.py`**:
   - Executes ETL pipeline from CSV/JSON billing data or live Boto3 polling into normalized DuckDB tables.
2. **`query_engine_tool.py`**:
   - Accepts plain-English questions, sends cached DuckDB schema to Claude, executes returned SQL, and synthesizes contextual explanations.
3. **`waste_analyzer_tool.py`**:
   - Executes multi-dimensional SQL scans over DuckDB and applies Claude reasoning across compute (ECS/EC2), serverless (Lambda), storage (S3), and database (RDS) resources.
4. **`guardrails_tool.py`**:
   - Evaluates optimization proposals against banking compliance rules (`RULE_S3_KMS`, `RULE_ECS_SIDECARS`, `RULE_LAMBDA_BOUNDS`, `RULE_NO_PUBLIC_ACCESS`).
5. **`iac_generator_tool.py`**:
   - Leverages Claude 3.5/3.7 Sonnet code generation to author valid, formatted AWS CloudFormation templates ready for AWS Service Catalog portfolio integration.
6. **`aws_connector_tool.py`**:
   - Interfaces with AWS Cost Explorer, CloudWatch, ECS, Lambda, and S3 APIs using federated IAM execution roles.

### 6.3 `agent-sdk-example/` (Anthropic Agent SDK Framework)
- **`finops_autonomous_agent.py`**:
  - Implements an autonomous multi-turn FinOps agent using the Anthropic Agent SDK.
  - Maintains an iterative scratchpad/thought chain: `Plan -> Select Tool -> Execute Tool -> Evaluate Result -> Verify Guardrails -> Final Response`.
- **`evaluation/`**:
  - Golden benchmark dataset (`eval_benchmarks.json`) containing 50+ enterprise FinOps scenarios with ground-truth SQL and cost savings.
  - Automated evaluation script (`evaluate_accuracy.py`) measuring Text-to-SQL exact match, execution accuracy, guardrail interception rate, and latency.

---

## 7. Database Schema Specification (DuckDB)

### 7.1 Table: `daily_cost_summary`
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `line_item_id` | `VARCHAR` | Primary key / Unique billing record ID |
| `account_id` | `VARCHAR` | AWS Account ID (12-digit) |
| `usage_start_date` | `TIMESTAMP` | Start timestamp of usage |
| `resource_id` | `VARCHAR` | AWS Resource ARN or Resource ID |
| `resource_type` | `VARCHAR` | Service type (`ECS-EC2`, `AWS-Lambda`, `S3`, `RDS`, `DynamoDB`, `VPC-NAT`) |
| `business_unit` | `VARCHAR` | Business Unit Tag (`Marketing`, `Engineering`, `DataScience`) |
| `daily_cost` | `DOUBLE` | Unblended cost in USD |
| `usage_amount` | `DOUBLE` | Usage quantity (vCPU-hours, GB-hours, Invocations) |

### 7.2 Table: `ecs_container_metrics`
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `task_arn` | `VARCHAR` | ECS Task ARN |
| `cluster_name` | `VARCHAR` | ECS Cluster Name |
| `service_name` | `VARCHAR` | ECS Service Name |
| `account_id` | `VARCHAR` | AWS Account ID |
| `business_unit` | `VARCHAR` | Associated Business Unit |
| `cpu_reserved` | `INTEGER` | Reserved CPU units (1024 = 1 vCPU) |
| `memory_reserved` | `INTEGER` | Reserved Memory in MiB |
| `cpu_utilization_p95` | `DOUBLE` | 95th percentile peak CPU utilization % |
| `memory_utilization_p95` | `DOUBLE` | 95th percentile peak Memory utilization % |
| `launch_type` | `VARCHAR` | Launch type (`EC2`) |
| `has_security_sidecar` | `BOOLEAN` | True if mandatory security sidecar is attached |

### 7.3 Table: `lambda_function_metrics`
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `function_arn` | `VARCHAR` | Lambda Function ARN |
| `function_name` | `VARCHAR` | Lambda Function Name |
| `account_id` | `VARCHAR` | AWS Account ID |
| `business_unit` | `VARCHAR` | Associated Business Unit |
| `memory_allocated_mb` | `INTEGER` | Configured memory size in MB |
| `memory_max_used_mb` | `INTEGER` | Peak recorded memory usage in MB |
| `avg_duration_ms` | `DOUBLE` | Average execution duration in ms |
| `invocations_count` | `INTEGER` | Total invocations in measurement period |
| `provisioned_concurrency` | `INTEGER` | Configured provisioned concurrency |
| `timeout_seconds` | `INTEGER` | Configured execution timeout in seconds |

### 7.4 Table: `s3_bucket_metrics`
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `bucket_name` | `VARCHAR` | S3 Bucket Name |
| `account_id` | `VARCHAR` | AWS Account ID |
| `business_unit` | `VARCHAR` | Associated Business Unit |
| `kms_key_arn` | `VARCHAR` | AWS Managed / Customer KMS Key ARN |
| `is_kms_encrypted` | `BOOLEAN` | True if SSE-KMS encryption is active |
| `storage_bytes_standard` | `BIGINT` | Bytes stored in S3 Standard class |
| `storage_bytes_glacier` | `BIGINT` | Bytes stored in S3 Glacier/IA class |
| `object_count` | `BIGINT` | Total object count in bucket |
| `has_lifecycle_policy` | `BOOLEAN` | True if lifecycle transition rules exist |
| `public_access_blocked` | `BOOLEAN` | True if all 4 public access block settings are active |

### 7.5 Table: `candidate_recommendations`
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `recommendation_id` | `VARCHAR` | Unique ID for waste recommendation |
| `account_id` | `VARCHAR` | AWS Account ID |
| `resource_id` | `VARCHAR` | Target AWS Resource ARN |
| `service_type` | `VARCHAR` | Service category (`ECS-EC2`, `Lambda`, `S3`, `RDS`) |
| `estimated_monthly_savings` | `DOUBLE` | Estimated cost reduction ($ USD / month) |
| `proposed_fix_description` | `VARCHAR` | Summary of proposed optimization |
| `compliance_status` | `VARCHAR` | `APPROVED` or `REJECTED_KMS_MANDATE` / `REJECTED_SECURITY_POLICY` |
| `guardrail_rule_triggered` | `VARCHAR` | Specific policy rule ID evaluated |

---

## 8. Enterprise Banking Compliance & Security Specification

```mermaid
flowchart TD
    Candidate[AI Candidate Recommendation] --> Interceptor[Banking Guardrails Engine]
    
    Interceptor --> R1{Rule 1: S3 KMS Key Check\nDoes recommendation disable/downgrade KMS?}
    R1 -- Yes --> V1[Reject: REJECTED_KMS_MANDATE\nLog Policy Violation]
    R1 -- No --> R2{Rule 2: ECS Sidecar Check\nDoes recommendation remove security sidecars?}
    
    R2 -- Yes --> V2[Reject: REJECTED_ECS_SIDECAR\nLog Policy Violation]
    R2 -- No --> R3{Rule 3: Lambda Telemetry Check\nDoes memory cut violate minimum buffer or X-Ray?}
    
    R3 -- Yes --> V3[Reject: REJECTED_LAMBDA_BOUNDS\nLog Policy Violation]
    R3 -- No --> R4{Rule 4: Zero Public Access Check\nDoes S3 remediation enforce BlockPublicPolicy?}
    
    R4 -- No --> V4[Reject: REJECTED_PUBLIC_ACCESS\nLog Policy Violation]
    R4 -- Yes --> Approved[Approve Recommendation\nEmit Compliance Pass Badge\nEnable CloudFormation Synthesis]
```

### Policy Rules Specification:
1. **`RULE_S3_KMS`**:
   - **Mandate**: S3 lifecycle and storage tiering optimizations must retain `BucketEncryption` with `ServerSideEncryptionRule` using AWS KMS (`aws_kms_key`).
   - **Violation Action**: Intercept and reject with violation code `REJECTED_KMS_MANDATE`.
2. **`RULE_ECS_SIDECARS`**:
   - **Mandate**: Container task resizing must preserve all security monitoring, audit logging, and intrusion detection container definitions in `AWS::ECS::TaskDefinition`.
   - **Violation Action**: Intercept and reject with violation code `REJECTED_ECS_SIDECAR`.
3. **`RULE_LAMBDA_BOUNDS`**:
   - **Mandate**: Memory optimization must maintain minimum memory thresholds required for enterprise tracing layers (AWS X-Ray / banking telemetry) and prevent execution timeouts.
   - **Violation Action**: Intercept and reject with violation code `REJECTED_LAMBDA_BOUNDS`.
4. **`RULE_NO_PUBLIC_ACCESS`**:
   - **Mandate**: S3 bucket modifications must explicitly enforce `PublicAccessBlockConfiguration` with `BlockPublicAcls: true`, `IgnorePublicAcls: true`, `BlockPublicPolicy: true`, and `RestrictPublicBuckets: true`.
   - **Violation Action**: Intercept and reject with violation code `REJECTED_PUBLIC_ACCESS`.

---

## 9. Security, Secrets Management, and Data Privacy

1. **Anthropic API Privacy & Zero-Retention**:
   - Direct integration via official `anthropic` SDK adheres to enterprise data privacy agreements ensuring customer cloud financial telemetry is never used for foundation model training.
2. **Secrets & Credentials Management**:
   - `ANTHROPIC_API_KEY`, `AWS_ACCESS_KEY_ID`, and session tokens are strictly loaded from environment variables (`.env`) or AWS Secrets Manager.
   - `.env` is permanently excluded via `.gitignore`.
3. **Data Masking & Account Isolation**:
   - In multi-tenant enterprise environments, account IDs and resource ARNs are validated against `accounts.json` registry to enforce role-based access control.

---

*CloudIntel System Architecture Specification — Standardized on Claude Code Plugin & Anthropic Agent SDK.*
