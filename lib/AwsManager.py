import logging
import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd
from sqlalchemy import create_engine, text
import json


class AwsManager:
    def upload_file(file_name, bucket, object_name=None):
        """
        Upload a file to an S3 bucket
        -
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.client("s3")
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def rds_server():
        # engine info
        DATABASE_TYPE = "postgresql"
        DBAPI = "psycopg2"
        HOST = "database-1.cta7zgbteazn.eu-west-2.rds.amazonaws.com"
        USER = "postgres"
        PASSWORD = "cFl7watx9juQY2Sn7cmh"
        DATABASE = "whiskyexchange"
        PORT = 5432
        engine = create_engine(
            f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        )

        print("Connected to RDS server")
        return engine

    def insert_row(spirit, rds_server):
        """
        Add the spirit profile to the database on amazon RDS server. Inserting the data as a row in the table by normalising the dictionary.
        -
        spirit: python dataclass to be converted to dictionary then sqlalchemy object.
        rds_server: the destination RDS server engine
        """

        data = spirit.__dict__

        df = pd.json_normalize(data)

        # normalized columns have full stop incompatible with SQL column headers so are replaced with underscore and lowercased.

        for col in df.columns:
            df.rename(
                columns={col: col.lower().replace(".", "_").replace(" ", "_")},
                inplace=True,
            )

        with rds_server.connect().execution_options(autocommit=True) as conn:
            df.to_sql("scotch_whisky", con=conn, if_exists="append", index=False)

        print(f"{spirit.product_id} added to RDS database")

    def rds_exists_check(id, rds_server):

        sql = f"""
            SELECT product_id FROM scotch_whisky
            WHERE product_id = '{id}';
        """
        with rds_server.connect().execution_options(autocommit=True) as conn:
            query = conn.execute(text(sql))

        db = pd.DataFrame(query)
        exists = not db.empty
        return exists
