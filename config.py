import os


class Config(object):
    ACCESS_KEY = os.environ.get('ACCESS_KEY', None)  # 'AKIAYZC4W6OAA337D5E6'
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    S3_BUCKET = os.environ.get('S3_BUCKET', None)
    TABLE_NAME = os.environ.get('TABLE_NAME', None)
