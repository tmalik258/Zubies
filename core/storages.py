from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestFilesMixin

class MediaStore(S3Boto3Storage):
    location = 'media'
    file_overwrite = True

class StaticManifestS3Storage(ManifestFilesMixin, S3Boto3Storage):
    location = 'static'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def hashed_name(self, name, content=None, filename=None):
        return super().hashed_name(name, content, filename)