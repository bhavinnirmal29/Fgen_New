from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import os

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    default_acl = 'public-read'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

class StaticStorage(S3Boto3Storage):
    location = 'static'
    file_overwrite = True
    default_acl = 'public-read'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

def get_storage_backend():
    """
    Returns the appropriate storage backend based on environment
    """
    if settings.DEBUG:
        return 'django.core.files.storage.FileSystemStorage'
    else:
        return 'new_App.storage.MediaStorage'
