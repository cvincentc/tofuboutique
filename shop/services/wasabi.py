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
    s3_url = env('AWS_S3_ENDPOINT_URL')
    bucket_name = env('AWS_STORAGE_BUCKET_NAME')
    s3 = boto3.resource('s3',
        endpoint_url= s3_url,
        aws_access_key_id=env('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY'))
    bucket = s3.Bucket(bucket_name)
    bucket.upload_fileobj(file, file_name)
    return '/'.join([s3_url, bucket_name, file_name])
        
