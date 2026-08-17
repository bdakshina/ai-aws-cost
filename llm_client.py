import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama-3.3-70b-versatile")

def call_llm(prompt: str, system_prompt: str = "You are CloudIntel FinOps AI Assistant.") -> str:
    """Calls Groq Cloud API if key is present, otherwise returns heuristic fallback response."""
    if GROQ_API_KEY and GROQ_API_KEY != "gsk_your_groq_api_key_here":
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Groq API call failed: {e}. Falling back to heuristic engine.")

    # Heuristic Fallback Engine
    return fallback_llm_response(prompt, system_prompt)

def fallback_llm_response(prompt: str, system_prompt: str) -> str:
    """Heuristic fallback engine when API key is missing or API call fails."""
    prompt_lower = prompt.lower()
    
    # 1. Text-to-SQL Fallbacks
    if "text-to-sql" in system_prompt.lower() or "generate sql" in prompt_lower or "select" in system_prompt.lower():
        if "lambda" in prompt_lower and ("expensive" in prompt_lower or "cost" in prompt_lower or "top" in prompt_lower):
            return "SELECT function_name, business_unit, memory_allocated_mb, memory_max_used_mb, (daily_cost * 30) AS estimated_monthly_cost FROM lambda_metrics JOIN raw_cost_reports ON lambda_metrics.function_arn = raw_cost_reports.resource_id ORDER BY estimated_monthly_cost DESC LIMIT 5;"
        elif "s3" in prompt_lower or "lifecycle" in prompt_lower or "bucket" in prompt_lower:
            return "SELECT bucket_name, business_unit, (storage_bytes_standard / 1e12) AS standard_tb, oldest_object_age_days, has_lifecycle_policy FROM s3_storage_metrics WHERE has_lifecycle_policy = FALSE ORDER BY standard_tb DESC;"
        elif "ecs" in prompt_lower or "container" in prompt_lower:
            return "SELECT task_arn, service_name, business_unit, cpu_reserved, cpu_utilization_max, memory_reserved, memory_utilization_max FROM ecs_task_metrics WHERE cpu_utilization_max < 15.0 ORDER BY cpu_reserved DESC;"
        elif "marketing" in prompt_lower:
            return "SELECT resource_type, resource_id, SUM(daily_cost) AS total_cost FROM raw_cost_reports WHERE business_unit = 'Marketing' GROUP BY resource_type, resource_id ORDER BY total_cost DESC;"
        else:
            return "SELECT resource_type, business_unit, SUM(daily_cost) AS total_cost FROM raw_cost_reports GROUP BY resource_type, business_unit ORDER BY total_cost DESC LIMIT 10;"

    # 2. IaC Generation Fallbacks
    if "cloudformation" in system_prompt.lower() or "template" in prompt_lower:
        return """AWSTemplateFormatVersion: '2010-09-09'
Description: 'CloudIntel Guardrail-Compliant AWS CloudFormation Remediation Template'

Parameters:
  Environment:
    Type: String
    Default: 'production'
    AllowedValues: ['development', 'staging', 'production']

Resources:
  CompliantS3BucketLifecyclePolicy:
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: 'mktg-campaign-raw-logs-2026'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: 'aws:kms'
              KMSMasterKeyID: 'arn:aws:kms:us-east-1:123456789012:key/k8f9a2b1-1111-2222-3333-mktg-key'
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: TransitionOldLogsToGlacier
            Status: Enabled
            Transitions:
              - TransitionInDays: 90
                StorageClass: GLACIER

Outputs:
  TemplateStatus:
    Value: 'GUARDRAIL_COMPLIANT_KMS_PRESERVED'
"""

    # 3. Context Synthesis Fallbacks
    return f"Based on the analytical database results, CloudIntel identified significant cost optimization opportunities. The primary spend driver is over-provisioned compute and un-tiered storage across Marketing and DataScience BUs. Applying the suggested compliance-vetted remediation will safely reduce monthly expenditure without altering security KMS keys or sidecars."
