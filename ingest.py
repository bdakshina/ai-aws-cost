import os
import json
import pandas as pd
import duckdb

DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")
DATA_PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")
DUCKDB_PATH = os.path.join(DATA_PROCESSED_DIR, "cloudintel.duckdb")

def init_db(con):
    """Create target DuckDB tables if they do not exist."""
    con.execute("""
    CREATE TABLE IF NOT EXISTS raw_cost_reports (
        line_item_id VARCHAR PRIMARY KEY,
        usage_start_date TIMESTAMP,
        resource_id VARCHAR,
        resource_type VARCHAR,
        business_unit VARCHAR,
        daily_cost DOUBLE,
        usage_amount DOUBLE
    );
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS ecs_task_metrics (
        task_arn VARCHAR PRIMARY KEY,
        cluster_name VARCHAR,
        service_name VARCHAR,
        business_unit VARCHAR,
        cpu_reserved INTEGER,
        memory_reserved INTEGER,
        cpu_utilization_max DOUBLE,
        memory_utilization_max DOUBLE,
        launch_type VARCHAR,
        has_security_sidecar BOOLEAN
    );
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS lambda_metrics (
        function_arn VARCHAR PRIMARY KEY,
        function_name VARCHAR,
        business_unit VARCHAR,
        memory_allocated_mb INTEGER,
        memory_max_used_mb INTEGER,
        avg_duration_ms DOUBLE,
        invocations_count INTEGER,
        timeout_seconds INTEGER
    );
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS s3_storage_metrics (
        bucket_name VARCHAR PRIMARY KEY,
        business_unit VARCHAR,
        kms_key_arn VARCHAR,
        is_kms_encrypted BOOLEAN,
        storage_bytes_standard BIGINT,
        storage_bytes_glacier BIGINT,
        object_count BIGINT,
        has_lifecycle_policy BOOLEAN,
        oldest_object_age_days INTEGER
    );
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS candidate_recommendations (
        recommendation_id VARCHAR PRIMARY KEY,
        resource_id VARCHAR,
        service_type VARCHAR,
        business_unit VARCHAR,
        estimated_monthly_savings DOUBLE,
        proposed_fix_description VARCHAR,
        compliance_status VARCHAR,
        guardrail_rule_triggered VARCHAR
    );
    """)

def ingest_data():
    """Main ETL pipeline reading raw billing & metric data and storing in DuckDB."""
    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
    con = duckdb.connect(DUCKDB_PATH)
    init_db(con)

    print("[Week 1 ETL] Starting Data Ingestion Pipeline...")

    # 1. Ingest CUR CSV Data
    cur_file = os.path.join(DATA_RAW_DIR, "aws_cur_export.csv")
    if os.path.exists(cur_file):
        df_cur = pd.read_csv(cur_file)
        con.execute("DELETE FROM raw_cost_reports;")
        con.register("df_cur_temp", df_cur)
        con.execute("""
            INSERT INTO raw_cost_reports
            SELECT line_item_id, CAST(usage_start_date AS TIMESTAMP), resource_id, resource_type, business_unit, daily_cost, usage_amount
            FROM df_cur_temp;
        """)
        con.unregister("df_cur_temp")
        print(f"  - Loaded {len(df_cur)} records into 'raw_cost_reports'")

    # 2. Ingest ECS Task Metrics JSON Data
    ecs_file = os.path.join(DATA_RAW_DIR, "ecs_task_metrics.json")
    if os.path.exists(ecs_file):
        with open(ecs_file, "r") as f:
            ecs_data = json.load(f)
        df_ecs = pd.DataFrame(ecs_data)
        con.execute("DELETE FROM ecs_task_metrics;")
        con.register("df_ecs_temp", df_ecs)
        con.execute("""
            INSERT INTO ecs_task_metrics
            SELECT task_arn, cluster_name, service_name, business_unit, cpu_reserved, memory_reserved, cpu_utilization_max, memory_utilization_max, launch_type, has_security_sidecar
            FROM df_ecs_temp;
        """)
        con.unregister("df_ecs_temp")
        print(f"  - Loaded {len(df_ecs)} records into 'ecs_task_metrics'")

    # 3. Ingest Lambda Metrics JSON Data
    lambda_file = os.path.join(DATA_RAW_DIR, "lambda_metrics.json")
    if os.path.exists(lambda_file):
        with open(lambda_file, "r") as f:
            lambda_data = json.load(f)
        df_lambda = pd.DataFrame(lambda_data)
        con.execute("DELETE FROM lambda_metrics;")
        con.register("df_lambda_temp", df_lambda)
        con.execute("""
            INSERT INTO lambda_metrics
            SELECT function_arn, function_name, business_unit, memory_allocated_mb, memory_max_used_mb, avg_duration_ms, invocations_count, timeout_seconds
            FROM df_lambda_temp;
        """)
        con.unregister("df_lambda_temp")
        print(f"  - Loaded {len(df_lambda)} records into 'lambda_metrics'")

    # 4. Ingest S3 Storage Metrics JSON Data
    s3_file = os.path.join(DATA_RAW_DIR, "s3_storage_metrics.json")
    if os.path.exists(s3_file):
        with open(s3_file, "r") as f:
            s3_data = json.load(f)
        df_s3 = pd.DataFrame(s3_data)
        con.execute("DELETE FROM s3_storage_metrics;")
        con.register("df_s3_temp", df_s3)
        con.execute("""
            INSERT INTO s3_storage_metrics
            SELECT bucket_name, business_unit, kms_key_arn, is_kms_encrypted, storage_bytes_standard, storage_bytes_glacier, object_count, has_lifecycle_policy, oldest_object_age_days
            FROM df_s3_temp;
        """)
        con.unregister("df_s3_temp")
        print(f"  - Loaded {len(df_s3)} records into 's3_storage_metrics'")

    con.close()
    print("[Week 1 ETL] Ingestion completed successfully! Database ready at:", DUCKDB_PATH)

if __name__ == "__main__":
    ingest_data()
