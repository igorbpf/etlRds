import os
import sys
import logging
from read_secret import get_secret
import pymysql
import pandas as pd
from lambda_decorators import cors_headers, dump_json_body

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

# rds settings
user, password, host, db_name, db_port = get_secret()

region_name = os.environ.get("REGION_NAME", "")

try:
    conn = pymysql.connect(host=host, user=user,
                           password=password, database=db_name, port=db_port, connect_timeout=10)
except pymysql.MySQLError as e:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


@dump_json_body
@cors_headers
def handler(event, context):
    """
    This function gets data from MySQL RDS instance
    """
    try:
        with conn.cursor() as cur:
            cur.execute("show tables;")
            resp = cur.fetchall()
            logger.info("***********************************")
            logger.info(host)
            logger.info(db_name)
            logger.info(resp)
            logger.info("***********************************")

        table_name = event.get("pathParameters").get("id")
        sql = f"""SELECT * FROM {table_name};"""
        df = pd.read_sql(sql, con=conn)
        data = list(df.T.to_dict().values())
        # create a response
        return {'statusCode': 200,
                'body': data}
    except Exception as e:
        logger.error(e)
        return {'statusCode': 400,
                'body': {'error_message': str(e)}}


if __name__ == '__main__':
    print(handler('', ''))
