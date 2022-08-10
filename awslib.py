#    _|_
#   /@-@\ Copyright © OpsBeacon, Inc.
#   \ - /    All rights reserved.
#    };{
 
import logging
import boto3
from botocore.exceptions import ClientError
import os

import csv
from io import StringIO

def get_all_aws_regions():
    regions = []
    for region in boto3.client('ec2', region_name = 'ap-south-1').describe_regions()['Regions']:
        regions.append(region['RegionName'])
    return regions

def list_ec2_instances(filters=[], instance_ids=[]):
    instances = []
    for region in get_all_aws_regions():
        instances += list_ec2_instances_region(region, filters, instance_ids)
    return instances

def list_ec2_instances_region(region, filters=[], instance_ids=[]):
    instances = []
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(
        Filters=filters,
        InstanceIds=instance_ids
    )
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)
    return instances

def describe_ec2_instance(region, instance_id):
    ec2 = boto3.client('ec2', region_name=region)
    reservations = []

    try:
        response = ec2.describe_instances(
            InstanceIds=[instance_id]
        )
        reservations = response.get('Reservations', [])
    except ClientError as e:
        logging.error(e)
        if e.response["Error"]["Code"] == "InvalidInstanceID.NotFound":
            logging.error(f"describe_ec2_instance: {instance_id}:{region} does not exists - remove from InstanceDB")

    if reservations:
        instances = reservations[0].get('Instances', [])
        if instances:
            return instances[0]
    else:
        return


def sns_publish_message(topic_arn, message, region='eu-central-1'):
    logging.debug(f"sns_publish_message: {topic_arn} {message}")
    session = boto3.Session()
    client = session.client(service_name='sns', region_name=region)
    try:
        client.publish(TopicArn=topic_arn,Message=message)
    except Exception as e:
        logging.error(f"awslib:sns_publish_message: {e}")

def s3_delete_object(bucket, key):
    s3 = boto3.resource('s3')
    s3.Object(bucket, key).delete()

def s3_get_object(bucket_name, key_name):
    session = boto3.Session()
    client = session.client('s3')
    return client.get_object(Bucket=bucket_name, Key=key_name)

def s3_put_object(bucket, key, data):
    s3 = boto3.resource('s3')
    s3.Object(bucket, key).put(Body=data)

def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def create_presigned_url(bucket_name, object_name, expiration=3600, region_name="ap-south-1"):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param region_name: string
    :return: Presigned URL as string. If error, returns None.
    """


    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3', region_name=region_name, endpoint_url=f"https://s3.{region_name}.amazonaws.com")
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def csv_values_from_s3(bucket_name, key_name):
    """
    Reads a csv file from S3 and returns a list of values
    """
    session = boto3.Session()
    client = session.client('s3')
    object = client.get_object(Bucket=bucket_name, Key=key_name)

    values = []
    if(object):
        file_content= object['Body'].read().decode('utf-8')
        reader = csv.reader(StringIO(file_content))
        for row in reader:
            values.append(row)
    return values