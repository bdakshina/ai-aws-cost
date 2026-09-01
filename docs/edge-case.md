# CloudIntel — Corner Scenarios, Edge Cases & Resiliency Specification

---

## 1. Executive Summary

This document serves as the authoritative repository of all **corner scenarios, edge cases, failure modes, adversarial boundary conditions, and programmatic mitigation strategies** for the **CloudIntel Enterprise AI FinOps Platform & Claude Code Plugin Architecture (`claude-code-plugins`)**.

It provides explicit failure definitions, risk severity levels, and automated defense mechanisms derived from [`docs/PROBLEM_STATEMENT.md`](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/PROBLEM_STATEMENT.md), [`docs/ARCHITECTURE.md`](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/ARCHITECTURE.md), [`docs/Implementation-plan.md`](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/Implementation-plan.md), and [`docs/deployment-plan.md`](file:///j:/AI_Learnings/ai-aws-cost/Automation/docs/deployment-plan.md).

---

## 2. Comprehensive Edge Case Matrix

| ID | Component Area | Corner Scenario / Edge Case | Risk Severity | Primary Programmatic Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **EC-01** | Data Ingestion (`data_ingest_tool.py`) | Untagged or Unknown Business Unit Resources in CUR / Logs | **MEDIUM** | Assign to `BU_UNALLOCATED` default partition and flag in compliance governance audit logs. |
| **EC-02** | Data Ingestion (`data_ingest_tool.py`) | Negative Spend, Promotional Credits & Zero-Cost Usage Lines | **LOW** | Filter out zero-usage records; isolate gross unblended cost from AWS promotional credits to avoid distorted savings calculations. |
| **EC-03** | Data Ingestion (`data_ingest_tool.py`) | Corrupted Raw CSVs, Missing Headers, or Malformed JSON Lines | **HIGH** | Strict Pydantic schema validation; invalid records logged to `ingest_errors.log` while processing remaining valid rows without halting. |
| **EC-04** | Analytical DB (`cloudintel.duckdb`) | DuckDB Single-Writer File Locking Collision during CLI Query | **HIGH** | Use read-only connection mode (`read_only=True`) for all query/analyzer tools; acquire exclusive write lock only during batch ingestion. |
| **EC-05** | Claude Cognitive (`claude_client.py`) | Anthropic Claude API Rate Limiting (HTTP 429) or Network Timeout | **HIGH** | Exponential backoff retry handler via `tenacity` (up to 4 retries) with automatic fallback to `claude-3-5-haiku-20241022`. |
| **EC-06** | Claude Cognitive (`claude_client.py`) | Large Multi-Account Ingestion Context Overflow (>200K Tokens) | **MEDIUM** | Analytical pre-aggregation in DuckDB before passing contextual summaries to Claude API context. |
| **EC-07** | Query Engine (`query_engine_tool.py`) | Destructive / Non-SELECT SQL Generation (SQL Injection Defense) | **CRITICAL** | AST / Regex SQL validator strictly enforcing read-only `SELECT` / `WITH` statements before DuckDB execution. |
| **EC-08** | Query Engine (`query_engine_tool.py`) | Empty SQL Query Result Set (0 Rows Returned for Query) | **LOW** | Intercept empty DataFrame before second-stage synthesis; return standard deterministic message without triggering LLM hallucination. |
| **EC-09** | Agent SDK (`finops_autonomous_agent.py`)| Infinite Tool Calling Loop in Multi-Turn Agent Reasoning | **HIGH** | Hard ceiling on agent recursion depth (`max_iterations = 6`) with forced synthesis of best-effort findings. |
| **EC-10** | Waste Analyzer (`waste_analyzer_tool.py`)| Burst / Spiky Workloads (99% Peak CPU for 1 Hour / Month) | **HIGH** | Evaluate 14-day P95/P99 percentiles alongside peak utilization; mark burst workloads as `BURST_CAPABLE_DO_NOT_RESIZE`. |
| **EC-11** | Waste Analyzer (`waste_analyzer_tool.py`)| Zero Invocations with Configured Provisioned Concurrency | **MEDIUM** | Dedicated pattern rule flagging `IDLE_PROVISIONED_CONCURRENCY` with exact calculation of zero-utilization monthly waste. |
| **EC-12** | Guardrails Engine (`guardrails_tool.py`)| Adversarial Prompt Injection Attempting S3 KMS Key Removal | **CRITICAL** | Programmatic rule interceptor (`RULE_S3_KMS`) forcing immediate status `REJECTED_KMS_MANDATE`. |
| **EC-13** | Guardrails Engine (`guardrails_tool.py`)| ECS Container Sidecar Removal during Task Resizing | **CRITICAL** | AST validator ensuring `AWS::ECS::TaskDefinition` retains mandatory security monitoring and telemetry container definitions. |
| **EC-14** | Guardrails Engine (`guardrails_tool.py`)| S3 Lifecycle Template Stripping Public Access Block | **HIGH** | Forceful programmatic injection of `PublicAccessBlockConfiguration` block into all generated S3 CloudFormation templates. |
| **EC-15** | IaC Generator (`iac_generator_tool.py`)| Malformed CloudFormation YAML / Service Catalog Schema Mismatch | **HIGH** | Clean markdown fencing and validate template syntax with `cfn-lint` and `yaml.safe_load()` prior to output. |
| **EC-16** | AWS Connector (`aws_connector_tool.py`)| Invalid, Expired AWS Credentials, or STS AssumeRole Failure | **HIGH** | Catch `ClientError` / `UnrecognizedClientException`, log diagnostic advice, and gracefully fallback to local synthetic dataset. |
| **EC-17** | Claude Code CLI (`.claude/`) | Unsupported or Malformed Slash Command Arguments | **LOW** | Display contextual help text with exact usage examples for `/finops-query`, `/finops-analyze`, and `/finops-remediate`. |

---

## 3. Detailed Edge Case Specifications & Programmatic Mitigations

### 3.1 Claude API, Prompt Caching & Agent SDK Edge Cases

#### EC-05: Anthropic API Rate Limiting (HTTP 429) & Network Timeouts
- **Scenario**: During high-frequency batch analysis or concurrent developer queries, Anthropic API returns `429 Too Many Requests` or `529 Overloaded`.
- **Risk**: Failure of CLI slash commands and broken agent multi-turn reasoning loops.
- **Mitigation Strategy**:
  - `claude_client.py` uses `tenacity` to apply jittered exponential backoff:
    ```python
    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
    import anthropic

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1.5, min=2, max=15),
        retry=retry_if_exception_type((anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.InternalServerError))
    )
    def call_claude_messages_api(client, **kwargs):
        return client.messages.create(**kwargs)
    ```
  - For non-critical triage tasks, automatically route requests to fast fallback model `claude-3-5-haiku-20241022`.

#### EC-06: Prompt Caching Misses & Cache Eviction
- **Scenario**: Database schemas or banking guardrail rules change frequently, triggering continuous prompt cache misses and increased latency.
- **Risk**: Increased API token consumption and higher per-query cost.
- **Mitigation Strategy**:
  - Structure prompt messages into strictly stratified blocks:
    1. **Static Block** (`cache_control: {"type": "ephemeral"}`): Standard DuckDB table schemas, AWS pricing tables, and banking compliance rules.
    2. **Dynamic Block**: User query text, current timestamp, and target AWS Account ID.
  - Ensures static context remains cached across all multi-turn interactions.

#### EC-09: Infinite Tool Calling Loops in Autonomous Agent Workflows
- **Scenario**: `finops_autonomous_agent.py` encounters ambiguous SQL results and repeatedly issues iterative tool calls without converging to an answer.
- **Risk**: Excessive API token burn and execution timeout.
- **Mitigation Strategy**:
  - Enforce a strict iteration ceiling in the Agent SDK loop:
    ```python
    MAX_AGENT_ITERATIONS = 6

    for iteration in range(MAX_AGENT_ITERATIONS):
        response = claude_client.send_message(messages=conversation_history, tools=FINOPS_TOOLS)
        if response.stop_reason != "tool_use":
            return response.content
        # Execute tool calls ...
        if iteration == MAX_AGENT_ITERATIONS - 1:
            return "Agent reached maximum reasoning depth. Summary of partial findings: " + summarize_findings(conversation_history)
    ```

---

### 3.2 Data Ingestion & DuckDB Analytical Engine Edge Cases

#### EC-01: Untagged or Unknown Business Unit Resources
- **Scenario**: Ingested billing records or CloudWatch metrics have missing or empty `BusinessUnit` / `Environment` tags.
- **Risk**: Inaccurate cost attribution and skewing of cross-BU waste reports.
- **Mitigation Strategy**:
  - `data_ingest_tool.py` inspects tag metadata. If missing or null, normalizes the record to `business_unit = 'BU_UNALLOCATED'`.
  - In waste analysis, `BU_UNALLOCATED` resources are flagged with a dedicated tagging governance recommendation: `ENFORCE_RESOURCE_TAGGING`.

#### EC-02: Negative Cost Items, AWS EDP Credits, and Refunds
- **Scenario**: AWS CUR billing line items contain negative values (Enterprise Discount Program credits, savings plan adjustments, tax refunds).
- **Risk**: Negative values distorting average daily usage calculations and producing negative savings estimates.
- **Mitigation Strategy**:
  - Ingestion separates `unblended_cost` from `credit_amount`.
  - FinOps waste algorithms operate exclusively on gross positive usage consumption (`daily_cost > 0`).

#### EC-04: DuckDB Concurrent File Locking Collisions
- **Scenario**: A developer runs `/finops-query` while background ingestion (`data_ingest_tool.py`) is executing a write transaction against `cloudintel.duckdb`.
- **Risk**: DuckDB throws `IOException: Could not set lock on file`.
- **Mitigation Strategy**:
  - `query_engine_tool.py` and `waste_analyzer_tool.py` strictly open connections using `duckdb.connect(database_path, read_only=True)`.
  - Batch ingestion acquires the write lock only during the brief table swap window.

---

### 3.3 Natural Language Query & SQL Injection Defense

#### EC-07: Destructive or Non-SELECT SQL Injection Generation
- **Scenario**: Adversarial prompt injection or LLM hallucination produces destructive SQL (e.g., `DROP TABLE daily_cost_summary;` or `DELETE FROM candidate_recommendations;`).
- **Risk**: **CRITICAL**. Loss of analytical database records or unauthorized data modification.
- **Mitigation Strategy**:
  - Programmatic AST and keyword inspection blocks non-SELECT queries before execution:
    ```python
    def validate_sql_safety(sql_query: str) -> bool:
        cleaned = sql_query.strip().upper()
        # Strictly enforce query starts with SELECT or WITH
        if not (cleaned.startswith("SELECT") or cleaned.startswith("WITH")):
            return False
        # Block forbidden destructive statements
        forbidden_keywords = [
            "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE", 
            "TRUNCATE", "REPLACE", "PRAGMA", "ATTACH", "COPY"
        ]
        tokens = cleaned.split()
        return not any(kw in tokens for kw in forbidden_keywords)
    ```

#### EC-08: Empty SQL Query Result Sets (0 Rows Returned)
- **Scenario**: A syntactically valid SQL query returns 0 rows (e.g., querying Lambda spend for a BU that only runs ECS containers).
- **Risk**: Second-stage LLM synthesis attempting to hallucinate fictitious numbers.
- **Mitigation Strategy**:
  - If the query result DataFrame is empty (`len(df) == 0`), intercept execution before the synthesis prompt and return a clean deterministic explanation:
    *"No matching cost or telemetry records were found in the database for the specified criteria."*

---

### 3.4 Multi-Resource Waste Analyzer Edge Cases

#### EC-10: Spiky & Periodic Workload Over-Optimization
- **Scenario**: An ECS task or Lambda function runs heavy month-end financial reconciliation batch jobs (95% CPU/RAM for 2 hours once per month) but runs at 3% usage otherwise.
- **Risk**: Sizing algorithms incorrectly downscale the resource, causing out-of-memory (OOM) crashes during batch processing.
- **Mitigation Strategy**:
  - Sizing algorithms evaluate 14-day percentiles (P95/P99) alongside peak utilization.
  - If `cpu_utilization_p95 > 75%` or peak utilization > 85%, mark resource as `BURST_WORKLOAD_PRESERVE_ALLOCATION`.

#### EC-11: Idle Provisioned Concurrency with Zero Invocations
- **Scenario**: A Lambda function has provisioned concurrency enabled (incurring fixed hourly charges) but has zero invocations over a 30-day billing window.
- **Risk**: Standard duration/memory analysis misses the idle provisioned concurrency expense.
- **Mitigation Strategy**:
  - Query explicitly joins `invocations_count == 0` with `provisioned_concurrency > 0`.
  - Flags recommendation as `REMOVE_IDLE_PROVISIONED_CONCURRENCY` and calculates exact monthly savings based on AWS provisioned concurrency hourly rates.

---

### 3.5 Enterprise Banking Compliance & Security Guardrails

#### EC-12: Adversarial Attempt to Remove or Downgrade S3 KMS Encryption
- **Scenario**: Optimization prompt proposes removing AWS Managed KMS Keys (`aws_kms_key` / `SSE-KMS`) to eliminate KMS API request charges.
- **Risk**: **CRITICAL**. Severe violation of banking security and regulatory data protection mandates.
- **Mitigation Strategy**:
  - `guardrails_tool.py` programmatically inspects all candidate optimizations:
    ```python
    def validate_s3_kms_mandate(candidate_fix: dict) -> str:
        desc = candidate_fix.get("proposed_fix_description", "").upper()
        cfn = candidate_fix.get("cloudformation_template", "").upper()
        if "REMOVE KMS" in desc or "DISABLE ENCRYPTION" in desc or "SSE-S3" in desc:
            return "REJECTED_KMS_MANDATE"
        if cfn and "AWS:KMS" not in cfn and "BUCKETENCRYPTION" in cfn:
            return "REJECTED_KMS_MANDATE"
        return "APPROVED"
    ```

#### EC-13: ECS Container Sidecar Stripping during Resizing
- **Scenario**: CloudFormation generation produces an updated `AWS::ECS::TaskDefinition` containing only the primary application container, omitting mandatory security monitoring or audit logging sidecars.
- **Risk**: **CRITICAL**. Loss of security observability, compliance auditing, and threat detection.
- **Mitigation Strategy**:
  - `guardrails_tool.py` compares container count in the original task definition against the proposed template.
  - If `has_security_sidecar == True`, verifies that all logging and monitoring containers are preserved in `ContainerDefinitions`. If missing, flags `REJECTED_ECS_SIDECAR`.

#### EC-14: Public S3 Bucket Exposure in Generated CloudFormation
- **Scenario**: An S3 lifecycle remediation template omits explicit public access block configurations.
- **Risk**: Potential data leakage upon deploying template to AWS.
- **Mitigation Strategy**:
  - `iac_generator_tool.py` forcefully injects the mandatory banking security block into every generated `AWS::S3::Bucket` resource:
    ```yaml
    PublicAccessBlockConfiguration:
      BlockPublicAcls: true
      BlockPublicPolicy: true
      IgnorePublicAcls: true
      RestrictPublicBuckets: true
    ```

---

### 3.6 CloudFormation Generation & AWS Connector Edge Cases

#### EC-15: Malformed CloudFormation YAML / Syntax Errors
- **Scenario**: Claude code generation includes markdown fencing ticks (` ```yaml ... ``` `) or incorrect YAML indentation in template strings.
- **Risk**: Rejection by AWS CloudFormation or AWS Service Catalog deployment failure.
- **Mitigation Strategy**:
  - Strip markdown code fences programmatically.
  - Validate template with `yaml.safe_load()` and `cfn-lint` before returning the template to Claude Code CLI or the user.

#### EC-16: Expired AWS Credentials or STS AssumeRole Denial
- **Scenario**: AWS session tokens expire during multi-account polling, or cross-account IAM role assumption fails.
- **Risk**: Ingestion pipeline crash.
- **Mitigation Strategy**:
  - Catch `botocore.exceptions.ClientError` and `botocore.exceptions.NoCredentialsError`.
  - Log diagnostic message indicating specific failed Account ID and IAM role ARN, and automatically fall back to local cached DuckDB data.

---

## 4. Verification & Automated Test Suites for Corner Scenarios

```bash
# Execute Full Corner Scenarios & Resilience Test Suite
pytest tests/security/test_banking_compliance.py -v
pytest tests/unit/test_query_agent.py -v
pytest tests/unit/test_analyzer.py -v
```

### Key Automated Assertions:
1. **Assertion 1 (KMS Removal Interception)**:
   - Input: Optimization recommendation proposing `Disable SSE-KMS to reduce KMS request cost`.
   - Result: `guardrails_tool.validate()` returns `status == "REJECTED_KMS_MANDATE"`.
2. **Assertion 2 (SQL Injection Prevention)**:
   - Input: Prompt producing `SELECT * FROM daily_cost_summary; DROP TABLE daily_cost_summary;`.
   - Result: `validate_sql_safety() == False`, query blocked with security log event.
3. **Assertion 3 (Public Access Block Enforcement)**:
   - Input: Generated S3 CloudFormation YAML template.
   - Result: Contains `BlockPublicAcls: true` and `BlockPublicPolicy: true`.
4. **Assertion 4 (Agent Iteration Ceiling)**:
   - Input: Mock tool returning ambiguous responses in an infinite loop.
   - Result: Agent halts cleanly at `iteration == 6` with partial findings summary.

---

*CloudIntel Corner Scenarios & Resiliency Specification — Standardized for Claude Code Plugins.*
