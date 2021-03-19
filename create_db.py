import os
import sys
import logging
from parser import parse_sql
from read_secret import get_secret
import boto3
import botocore
import pymysql

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

# rds settings
logger.info("get credentials")
user, password, host, db_name, db_port = get_secret()


region_name = os.environ.get("REGION_NAME", "")

# Resource S3
s3 = boto3.resource('s3', region_name=region_name,
                    config=botocore.config.Config(s3={'addressing_style': 'path'}))


try:
    logger.info("try connection")
    conn = pymysql.connect(host=host, user=user,
                           password=password, database=db_name, port=db_port, connect_timeout=10)

    logger.info("connected")
except pymysql.MySQLError as e:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def handler(event, context):
    """
    This function runs sql scripts in MySQL RDS instance
    """

    logger.info("Init function")

    bucket_name = os.environ.get('BUCKET_NAME', "")

    key = event['Records'][0]['s3']['object']['key']

    logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    logger.info(key)
    logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    object = s3.Object(bucket_name, key=key)
    file_stream = object.get()['Body'].read()

    stmts = parse_sql(file_stream)

    logger.info("#################################")
    logger.info(stmts)
    logger.info("#################################")

    with conn.cursor() as cur:
        for stmt in stmts:
            logger.info("***********************************")
            logger.info(stmt)
            logger.info("***********************************")
            cur.execute(stmt)
            conn.commit()

    logger.info("INFO: SQL script successfully submitted")

    return True


if __name__ == '__main__':
    print(handler('', ''))
