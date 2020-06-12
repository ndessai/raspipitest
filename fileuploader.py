
import logging
import boto3
from botocore.exceptions import ClientError
import uuid

from io import BytesIO
from time import sleep
from picamera import PiCamera


def create_bucket(bucket_name, region=None):
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(blob, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    # Upload the file
    s3 = boto3.resource('s3')
    try:
        response = s3.Object(bucket, object_name).put(ACL='public-read', Body=blob)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def capture_and_upload():
    folder_name = str(uuid.uuid1())
    
    camera = PiCamera()
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    image_streams = []
    for x in range(1,15):
        print("taking pic")
        camera.capture('foo.jpg')
        my_stream = BytesIO()
        camera.capture(my_stream, 'jpeg')
        my_stream.seek(0)
        image_streams.append(my_stream)

    x = 1
    for stream in image_streams:
        print("uploading pic")
        upload_file(stream, 'picar-workoutimages', folder_name + '/'+ str(x))
        x = x+1
        stream.close()

capture_and_upload()