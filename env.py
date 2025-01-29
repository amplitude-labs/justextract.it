import boto3
from botocore.exceptions import ClientError
import os


def setup_secrets():
    secret_name = "justextract-unkey-secrets"
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

    os.environ["UNKEY_API_ID"] = get_secret_value_response['UNKEY_API_ID']
    os.environ["UNKEY_ROOT_KEY"] = get_secret_value_response['UNKEY_ROOT_KEY']
