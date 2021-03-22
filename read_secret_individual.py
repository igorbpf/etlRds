import os
import base64
import logging
import boto3
import botocore


def get_secret(secret_name):

    region_name = os.environ.get("REGION_NAME", "sa-east-1")

    # Create a Secrets Manager client
    session = boto3.session.Session()

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        config=botocore.config.Config(s3={'addressing_style': 'path'})
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        if "SecretString" in get_secret_value_response:
            return get_secret_value_response["SecretString"]
        else:
            return base64.b64decode(get_secret_value_response["SecretString"])

    except Exception as e:
        logging.error("Unable to read secrets")
        logging.error(e)
    return None


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_secret(''))
