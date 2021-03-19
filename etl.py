import os
import sys
import codecs
import logging
import csv
from read_secret import get_secret
import boto3
import botocore
import pymysql


# rds settings
user, password, host, db_name, db_port = get_secret()

region_name = os.environ.get("REGION_NAME", "")

# Resource S3
s3 = boto3.resource('s3', region_name=region_name,
                    config=botocore.config.Config(s3={'addressing_style': 'path'}))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


try:
    conn = pymysql.connect(host=host, user=user,
                           password=password, database=db_name, port=db_port, connect_timeout=10)
except pymysql.MySQLError as e:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def insert_data(table_name, data, columns, key_columns):

    number_columns = len(columns)

    update_columns = columns.copy()

    for key_column in key_columns:
        update_columns.remove(key_column)

    number_update_columns = len(update_columns)

    column_str = ("""{},""" * number_columns)[:-1]
    column_str = column_str.format(*columns)

    insert_str = ("%s, " * number_columns)[:-2]

    update_str = ("""{}=%s, """ * number_update_columns)[:-2]

    update_str = update_str.format(*update_columns)

    final_str = "INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s " % (
        table_name, column_str, insert_str, update_str)

    with conn.cursor() as cur:
        for datum in data:
            cur.execute(final_str, datum)
        conn.commit()


def handler(event, context):
    """
    This function loads data into MySQL RDS instance
    """

    bucket_name = os.environ.get('BUCKET_NAME', "")

    key = event['Records'][0]['s3']['object']['key']

    object = s3.Object(bucket_name, key=key).get()

    # csvreader = DictReaderStrip(codecs.getreader("utf-8")(object["Body"]))
    csvreader = csv.reader(codecs.getreader(
        "utf-8")(object["Body"]), delimiter=",")

    # Init lists to populate tables
    data_cliente = []
    data_especialista = []

    for index, row in enumerate(csvreader):
        # populate lists
        if index:
            logger.info("***********************************")
            logger.info(row)
            logger.info("***********************************")

            data_cliente.append(
                (row[0], row[1], row[2], row[3], row[4], row[2], row[3], row[4]))

            data_especialista.append((row[4], row[5], row[5]))

    # Set columns and table name
    especialista_columns = ["funcional", "nome"]
    key_columns = ["funcional"]
    table_name = "Especialista"

    insert_data(table_name=table_name, data=data_especialista,
                columns=especialista_columns, key_columns=key_columns)

    cliente_columns = ["agencia", "conta", "nome", "saldo", "especialista_id"]
    key_columns = ["agencia", "conta"]
    table_name = "Cliente"

    insert_data(table_name=table_name, data=data_cliente,
                columns=cliente_columns, key_columns=key_columns)

    logger.info("INFO: Data successfully inserted")

    return True


if __name__ == '__main__':
    print(handler('', ''))
