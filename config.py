import boto3
import json
from botocore.exceptions import ClientError

def get_postgresql_secrets(secret_name="<secret-name>", region_name="us-east-1"):
    """
    Fetch PostgreSQL connection credentials from AWS Secrets Manager.

    Returns:
        dict: Dictionary with keys: username, password, host, port, dbname
    Raises:
        ClientError: If retrieval fails.
    """
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        response = client.get_secret_value(SecretId=secret_name)

        # Parse JSON-formatted secret string
        if 'SecretString' in response:
            secret_dict = json.loads(response['SecretString'])
            secret_dict["host"] = "<db-host>"
            secret_dict["port"] = "5432"
            secret_dict["dbname"] = "mini_inventory"

            return secret_dict
        else:
            raise ValueError("SecretString not found in response.")
    
    except ClientError as e:
        print(f"❌ Error retrieving secret from Secrets Manager: {e}")
        raise e

# Retrieve the secrets
secrets = get_postgresql_secrets()

# Build SQLAlchemy config from the secret
class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{secrets['username']}:{secrets['password']}@"
        f"{secrets['host']}:{secrets['port']}/{secrets['dbname']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
