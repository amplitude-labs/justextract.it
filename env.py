import json
import boto3
from botocore.exceptions import ClientError
import os


def get_secret(secret):
    secret_name = secret
    region_name = "ap-southeast-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)


def setup_secrets():
    nexai_rds_secrets = get_secret("justextract-unkey-secrets")
    os.environ["UNKEY_API_ID"] = nexai_rds_secrets["UNKEY_API_ID"]
    os.environ["UNKEY_ROOT_KEY"] = nexai_rds_secrets["UNKEY_ROOT_KEY"]
    os.environ["UNKEY_HARDCODED_KEY"] = nexai_rds_secrets["UNKEY_HARDCODED_KEY"]

    nexai_ai_secrets = get_secret("nexai-ai-secrets")
    os.environ["OPENAI_API_KEY"] = nexai_ai_secrets["openaiApiKey"]

    nexai_ai_secrets = get_secret("GEMINI_API_KEY")
    os.environ["GEMINI_API_KEY"] = nexai_ai_secrets["GEMINI_API_KEY"]
