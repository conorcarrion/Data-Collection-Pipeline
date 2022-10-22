from lib.AwsManager import AwsManager
import boto3

s3 = boto3.resource('s3')

s3_bucket = 'aicore-webscraper-cq'

AwsManager.upload_file('tests/url_list.text', s3_bucket)