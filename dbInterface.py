import boto3
import os
from botocore.exceptions import ClientError
import logging
import cx_Oracle as ora

class DbInterface:

    def __init__(self, tns_name: str, login: str, pwd: str):
        self.tns_name = tns_name
        self.login = login
        self.pwd = pwd
        self.db_open = False

        try:
            db = ora.connect(self.login, self.pwd, self.tns_name)
            self.db_open = True
        except Exception as err:
            self.db_open = False

    def is_open(self):
        return self.db_open

    def insert_search_result(self):
        pass


class MongoDbInterface:

    def __init__(self, client_name: str, db_name: str, coll_name: str):
        """Upload a file to a MongoDB database
        :param client_name: File to upload
        :param db_name: mongodb name
        :coll_name: collection name
        """
        self.client_name = client_name
        self.db_name = db_name
        self.coll_name = coll_name
        self.db_open = False

    def upload_result(self):
        """Upload a JSON result to Mongodb
        :return: True if file was uploaded, else False
        """

class S3BucketInterface:

    def __init__(self, file_name: str, bucket_name, object_name = None):
        """Constructor for uploading a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)
        self.s3_client = boto3.client('s3')


    def upload_file(self, file_name: str):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        try:
            response = self.s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True