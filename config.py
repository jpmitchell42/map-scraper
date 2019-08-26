import os


class Config(object):
    ACCESS_KEY = os.environ.get("ACCESS_KEY", "undefined")
    SECRET_KEY = os.environ.get("SECRET_KEY", "undefined")
    S3_BUCKET = os.environ.get("S3_BUCKET", "undefined")
    TABLE_NAME = os.environ.get("TABLE_NAME", "undefined")
