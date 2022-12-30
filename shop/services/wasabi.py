import boto3
from django.core.files.base import ContentFile
from django.utils.timezone import datetime
from django.db.models.fields.files import ImageFieldFile
from s3transfer.manager import TransferManager
import environ
env = environ.Env()
environ.Env.read_env()


def upload_fileobj(file, file_name = None):
    if file_name is None:
        file_name = datetime.now().strftime('%Y%m%d-%H%M%S')
    s3_url = 'https://s3.us-west-1.wasabisys.com'
    bucket_name = 'tofubtq-shop-images'
    s3_client = boto3.client('s3',
        endpoint_url= s3_url,
        aws_access_key_id='QUQ2HU9NFB08XSX1PD6Q',
        aws_secret_access_key='ArfeMTA3jMZuh6EgeFEgcBm4ywNJ2NpcEJkmsH9I'
    )
    s3 = boto3.resource('s3',
        endpoint_url= s3_url,
        aws_access_key_id='QUQ2HU9NFB08XSX1PD6Q',
        aws_secret_access_key='ArfeMTA3jMZuh6EgeFEgcBm4ywNJ2NpcEJkmsH9I')
    bucket = s3.Bucket(bucket_name)
    bucket.upload_fileobj(file, file_name)
    return '/'.join([s3_url, bucket_name, file_name])
        
